#!/usr/bin/env node
// Web and mobile checks in headless Chrome, run by scripts/check.sh. No dependencies: it talks to
// Chrome through the DevTools protocol over a pipe.
//
//   node scripts/viewports.mjs <base-url> <screenshot-dir> <page>...
//
// For every page at 320, 375, 768 (mobile emulation) and 1280 px (desktop): the page loads, no
// JavaScript errors, no failed requests to the site itself, no horizontal scrolling, a viewport meta
// tag. A full-page screenshot of each goes to <screenshot-dir>/<viewport>/<page>.png for human review.
// Chrome: $CHROME, or google-chrome / chromium on PATH, or the standard macOS location.
// Exit code: 0 = OK, 1 = problems found, 2 = the check could not run.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, dirname, join } from 'node:path';

const VIEWPORTS = [
    { name: 'mobile-320', width: 320, height: 640, mobile: true },
    { name: 'mobile-375', width: 375, height: 812, mobile: true },
    { name: 'tablet-768', width: 768, height: 1024, mobile: true },
    { name: 'desktop-1280', width: 1280, height: 800, mobile: false },
];
const LOAD_TIMEOUT_MS = 15000;
const SETTLE_MS = 300; // late layout: web fonts, images without dimensions
const MAX_SHOT_HEIGHT = 16000;

// Runs in the page: horizontal overflow (with the outermost elements that cause it) and viewport meta.
const MEASURE = `(() => {
    const doc = document.documentElement, vw = doc.clientWidth, wide = [];
    if (doc.scrollWidth > vw + 1) {
        for (const el of document.body.querySelectorAll('*')) {
            const r = el.getBoundingClientRect();
            if (r.width && (r.right > vw + 1 || r.left < -1) && !wide.some(w => w.el.contains(el))) {
                wide.push({ el, right: Math.round(r.right) });
            }
        }
    }
    const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
        [...el.classList].slice(0, 2).map(c => '.' + c).join('');
    return {
        vw, sw: doc.scrollWidth,
        meta: !!document.querySelector('meta[name="viewport"][content*="width=device-width"]'),
        wide: wide.slice(0, 5).map(w => name(w.el) + ' (right edge ' + w.right + 'px)'),
    };
})()`;

function fail(message) {
    console.error(`  cannot run the web and mobile checks: ${message}`);
    process.exit(2);
}

function findChrome() {
    if (process.env.CHROME) return existsSync(process.env.CHROME) ? process.env.CHROME : null;
    const names = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'];
    for (const dir of (process.env.PATH || '').split(delimiter)) {
        for (const n of names) if (dir && existsSync(join(dir, n))) return join(dir, n);
    }
    const mac = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    return existsSync(mac) ? mac : null;
}

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// True if `promise` resolves within `ms`, false if time runs out first. The timer is always cleared, so a
// time limit never fires later in the run.
async function within(promise, ms) {
    let timer;
    const expired = new Promise(resolve => { timer = setTimeout(() => resolve(false), ms); });
    try {
        return await Promise.race([promise.then(() => true), expired]);
    } finally {
        clearTimeout(timer);
    }
}

// Minimal DevTools protocol client: JSON messages separated by NUL on fds 3 (in) and 4 (out).
class Browser {
    constructor(binary) {
        this.profile = mkdtempSync(join(tmpdir(), 'frs-viewports-'));
        const args = ['--headless=new', '--remote-debugging-pipe', `--user-data-dir=${this.profile}`,
            '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-gpu',
            '--hide-scrollbars', '--mute-audio', '--disable-background-networking', '--disable-component-update',
            '--disable-sync', '--disable-default-apps', '--no-pings', 'about:blank'];
        if (process.env.CI) args.unshift('--no-sandbox'); // CI runners: throwaway VM, sandbox often unavailable
        this.proc = spawn(binary, args, { stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe'] });
        this.next = 0;
        this.pending = new Map();
        this.listeners = new Set();
        this.exited = false;
        this.closed = new Promise(resolve => { this.proc.on('exit', resolve); this.proc.on('error', resolve); });
        // Chrome gone (did not start, crashed, closed): every pending and later call fails with the reason.
        const gone = err => {
            this.exited = true;
            for (const waiter of this.pending.values()) waiter.reject(err);
            this.pending.clear();
        };
        this.proc.on('exit', code => gone(new Error(`${binary} exited (code ${code})`)));
        this.proc.on('error', err => gone(new Error(`${binary}: ${err.message}`)));
        this.proc.stdio[3].on('error', () => {}); // writing after Chrome exited: reported by 'exit'
        this.proc.stdio[4].on('error', () => {});
        this.proc.stderr.resume();
        let buffer = '';
        this.proc.stdio[4].setEncoding('utf8');
        this.proc.stdio[4].on('data', chunk => {
            buffer += chunk;
            let end;
            while ((end = buffer.indexOf('\0')) >= 0) {
                const message = JSON.parse(buffer.slice(0, end));
                buffer = buffer.slice(end + 1);
                const waiter = this.pending.get(message.id);
                if (waiter) {
                    this.pending.delete(message.id);
                    message.error ? waiter.reject(new Error(message.error.message)) : waiter.resolve(message.result);
                } else {
                    for (const listener of this.listeners) listener(message);
                }
            }
        });
    }

    send(method, params = {}, sessionId) {
        if (this.exited) return Promise.reject(new Error('Chrome is not running'));
        const id = ++this.next;
        const reply = new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
        this.proc.stdio[3].write(JSON.stringify({ id, method, params, sessionId }) + '\0');
        return reply;
    }

    async close() {
        try { await within(this.send('Browser.close'), 3000); } catch { /* already gone */ }
        if (this.proc.exitCode === null) this.proc.kill();
        await within(this.closed, 3000);
        // Chrome helper processes can write a little after the main process exits: retry for a few seconds.
        for (let i = 0; i < 20 && existsSync(this.profile); i++) {
            try { rmSync(this.profile, { recursive: true, force: true }); } catch { /* still in use */ }
            if (existsSync(this.profile)) await sleep(250);
        }
    }
}

async function checkPage(browser, url, viewport, shotPath) {
    const problems = [];
    const origin = new URL(url).origin;
    const pathOf = u => u.startsWith(origin) ? u.slice(origin.length) : u;
    // Requests the browser makes on its own (not referenced by the page) do not count.
    const ours = u => u.startsWith(origin) && pathOf(u) !== '/favicon.ico';
    const { targetId } = await browser.send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await browser.send('Target.attachToTarget', { targetId, flatten: true });
    const page = (method, params) => browser.send(method, params, sessionId);
    const requests = new Map();
    let loaded;
    const load = new Promise(resolve => { loaded = resolve; });
    const listener = ({ method, params, sessionId: from }) => {
        if (from !== sessionId) return;
        if (method === 'Page.loadEventFired') loaded();
        else if (method === 'Runtime.exceptionThrown') {
            const d = params.exceptionDetails;
            problems.push(`JavaScript error: ${(d.exception?.description || d.text || '').split('\n')[0]}`);
        } else if (method === 'Runtime.consoleAPICalled' && params.type === 'error') {
            problems.push(`console.error: ${params.args.map(a => a.value ?? a.description ?? '').join(' ').slice(0, 200)}`);
        } else if (method === 'Network.requestWillBeSent') requests.set(params.requestId, params.request.url);
        else if (method === 'Network.responseReceived') {
            const { status, url: u } = params.response;
            if (status >= 400 && ours(u)) problems.push(`HTTP ${status}: ${pathOf(u)}`);
        } else if (method === 'Network.loadingFailed' && !params.canceled) {
            const u = requests.get(params.requestId) || '';
            if (ours(u)) problems.push(`failed to load ${pathOf(u)} (${params.errorText})`);
        }
    };
    browser.listeners.add(listener);
    try {
        await page('Page.enable');
        await page('Runtime.enable');
        await page('Network.enable');
        await page('Emulation.setDeviceMetricsOverride',
            { width: viewport.width, height: viewport.height, deviceScaleFactor: 1, mobile: viewport.mobile });
        await page('Emulation.setTouchEmulationEnabled', { enabled: viewport.mobile });
        const nav = await page('Page.navigate', { url });
        if (nav.errorText) {
            problems.push(`does not load (${nav.errorText})`);
            return problems;
        }
        if (!await within(load, LOAD_TIMEOUT_MS)) problems.push(`load event not fired within ${LOAD_TIMEOUT_MS / 1000}s`);
        await sleep(SETTLE_MS);
        const { result } = await page('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
        const m = result.value;
        if (!m.meta) problems.push('no <meta name="viewport" content="width=device-width, ...">');
        if (m.sw > m.vw + 1) {
            problems.push(`horizontal scroll: page is ${m.sw}px wide in a ${m.vw}px viewport` +
                (m.wide.length ? `; too wide: ${m.wide.join(', ')}` : ''));
        }
        const { cssContentSize } = await page('Page.getLayoutMetrics');
        const height = Math.max(1, Math.min(Math.ceil(cssContentSize.height), MAX_SHOT_HEIGHT));
        const shot = await page('Page.captureScreenshot', {
            format: 'png', captureBeyondViewport: true,
            clip: { x: 0, y: 0, width: Math.max(viewport.width, Math.ceil(cssContentSize.width)), height, scale: 1 },
        });
        mkdirSync(dirname(shotPath), { recursive: true });
        writeFileSync(shotPath, Buffer.from(shot.data, 'base64'));
    } finally {
        browser.listeners.delete(listener);
        await browser.send('Target.closeTarget', { targetId }).catch(() => {});
    }
    return problems;
}

async function main() {
    const [base, shotDir, ...pages] = process.argv.slice(2);
    if (!base || !shotDir || pages.length === 0) fail('usage: viewports.mjs <base-url> <screenshot-dir> <page>...');
    const binary = findChrome();
    if (!binary) fail('Chrome not found: install Google Chrome or Chromium, or set CHROME=/path/to/chrome');
    const browser = new Browser(binary);
    let failures = 0;
    try {
        if (!await within(browser.send('Browser.getVersion'), 20000)) {
            throw new Error(`${binary} did not answer on the DevTools pipe`);
        }
        for (const viewport of VIEWPORTS) {
            let bad = 0;
            for (const pagePath of pages) {
                const url = new URL(pagePath, base).href;
                const shot = join(shotDir, viewport.name, pagePath.replace(/\.html?$/, '') + '.png');
                const problems = await checkPage(browser, url, viewport, shot);
                for (const p of [...new Set(problems)]) console.log(`  ${viewport.name}  ${pagePath}: ${p}`);
                if (problems.length) bad++;
            }
            console.log(`  ${viewport.name}: ${pages.length - bad}/${pages.length} pages OK`);
            failures += bad;
        }
    } finally {
        await browser.close();
    }
    process.exit(failures ? 1 : 0);
}

main().catch(err => fail(err.message));

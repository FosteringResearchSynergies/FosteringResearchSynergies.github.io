// Eleventy 3: sources in src/, output in _site/ (the only thing published, see docs/ROADMAP.md).
//   npm run build               # deletes _site/, then builds it
//   npm run dev -- --port=N     # local preview; a busy port is an error, never a silent switch
import yaml from "js-yaml";

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December"];
const WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

export default function (eleventyConfig) {
    // Data files in YAML (src/_data/*.yml). An empty or comment-only file is null. Unquoted dates
    // become JavaScript dates: the data files quote them ("2026-05-12").
    eleventyConfig.addDataExtension("yml,yaml", (contents) => yaml.load(contents) ?? null);

    // Static files, copied as they are. src/assets/ is served as /assets/; pictures/ and styles.css
    // belong to the pages ported from the old static site and keep their URLs.
    eleventyConfig.addPassthroughCopy("src/assets");
    eleventyConfig.addPassthroughCopy("src/pictures");
    eleventyConfig.addPassthroughCopy("src/styles.css");
    eleventyConfig.addPassthroughCopy("src/events/*.css");

    // Stops the build with a message, for templates that receive invalid arguments:
    // {{ "what went wrong" | fail }}
    eleventyConfig.addFilter("fail", (message) => {
        throw new Error(message);
    });

    // Items of a list whose key (dotted path allowed) equals a value:
    // {% set next = editions | where("status", "upcoming") | first %}
    eleventyConfig.addFilter("where", (list, key, value) =>
        (list || []).filter((item) => key.split(".").reduce((v, k) => (v == null ? v : v[k]), item) === value),
    );

    // Letters of a city for the classes chars-4 ... chars-12 of the CSS, which size a name to fill its
    // column: the length, between 4 and 12 (a missing city counts as 4). chars-{{ edition.city | fitChars }}
    eleventyConfig.addFilter("fitChars", (text) => Math.min(12, Math.max(4, String(text ?? "").length)));

    // Dates of an edition as one string, from the quoted "YYYY-MM-DD" values of the data files:
    // "18–20 December 2025", "30 November – 2 December 2026", "18 December 2025" (no end or same day).
    // "YYYY-MM" while only the month is known: "November 2023", "November – December 2023".
    // Returns "" when start is null: the template shows the TBA placeholder instead.
    eleventyConfig.addFilter("dateRange", (start, end) => {
        if (!start) return "";
        const parse = (value) => {
            const match = /^(\d{4})-(\d{2})(?:-(\d{2}))?$/.exec(String(value));
            if (!match) throw new Error(`dateRange: "${value}" is not a quoted "YYYY-MM-DD" or "YYYY-MM" date`);
            return { y: match[1], m: MONTHS[Number(match[2]) - 1], d: match[3] ? String(Number(match[3])) : null };
        };
        const a = parse(start);
        const b = end ? parse(end) : a;
        if (!a.d !== !b.d) throw new Error(`dateRange: "${start}" and "${end}" must have the same format`);
        if (!a.d) {
            if (a.y !== b.y) return `${a.m} ${a.y} – ${b.m} ${b.y}`;
            return a.m === b.m ? `${a.m} ${a.y}` : `${a.m} – ${b.m} ${b.y}`;
        }
        if (a.y !== b.y) return `${a.d} ${a.m} ${a.y} – ${b.d} ${b.m} ${b.y}`;
        if (a.m !== b.m) return `${a.d} ${a.m} – ${b.d} ${b.m} ${b.y}`;
        if (a.d !== b.d) return `${a.d}–${b.d} ${b.m} ${b.y}`;
        return `${a.d} ${a.m} ${a.y}`;
    });

    // Day of a program, for its heading: "Thursday 18 December", from a quoted "YYYY-MM-DD" value. The
    // year is left out: the dates of the edition give it. {{ day.date | dayDate }}
    eleventyConfig.addFilter("dayDate", (value) => {
        const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(value));
        if (!match) throw new Error(`dayDate: "${value}" is not a quoted "YYYY-MM-DD" date`);
        const date = new Date(Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3])));
        return `${WEEKDAYS[date.getUTCDay()]} ${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]}`;
    });

    // Label of an edition, the same in page titles and on the home: its name if it has one, otherwise
    // "FRS <year> · <City>" (no year while it is unknown, "TBA" for a missing city).
    // {{ edition | editionLabel(site.short_name) }}
    eleventyConfig.addFilter("editionLabel", (edition, shortName) =>
        edition.name || `${shortName}${edition.year ? " " + edition.year : ""} · ${edition.city || "TBA"}`,
    );

    // Public address of a page, the one search engines should list: the site URL plus the page path,
    // without a final "index.html" ("/index.html" -> ".../", "/press/index.html" -> ".../press/").
    // {{ page.url | canonical(site.url) }}
    eleventyConfig.addFilter("canonical", (url, base) => base + String(url).replace(/index\.html$/, ""));

    // scripts/preview.sh prints the URL before the server starts: the port must be the one asked for.
    eleventyConfig.setServerOptions({ portReassignmentRetryCount: 0 });
}

export const config = {
    dir: {
        input: "src",
        includes: "_includes",
        layouts: "_includes/layouts",
        data: "_data",
        output: "_site",
    },
    templateFormats: ["njk", "md", "html"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
};

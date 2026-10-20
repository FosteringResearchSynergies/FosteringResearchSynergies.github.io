#!/usr/bin/env python3
"""PreToolUse guard: keep agents off `main`, `deploy` and the main checkout.

Rules (see CLAUDE.md and the skills start-task and release):

- The main checkout (the one whose git dir is the common dir) is read-only for agents, whatever
  branch it is on. So is any checkout on `main` or `deploy`. There:
  - Edit/Write/MultiEdit/NotebookEdit are refused;
  - git is limited to read-only commands plus `fetch`, `merge --ff-only origin/main`,
    `pull --ff-only` (fast-forward to the upstream only), `worktree add/remove/prune/list`
    and `branch -d`. No `checkout -b`/`switch -c`: a task branch lives in its own worktree.
- In every checkout of this repository: no `checkout`/`switch` to main or deploy, no worktree on
  them, no rename, delete or force-move of them, no fetch that overwrites them.
- In any repository: `git push` is refused when it targets main or deploy (also through HEAD or @),
  forces (--force*, -f in a cluster, +refspec), deletes (--delete, -d in a cluster, :ref, --prune)
  or pushes many refs at once (--all, --branches, --mirror, refspecs with *).
- A `cd` or `git -C` target with $VAR or backticks cannot be resolved here, so the command is
  treated as if it ran in the main checkout: read-only git, fetch, worktree add/remove, branch -d
  and merge --ff-only origin/main pass; anything else is refused with a request for a literal path.

- Nothing goes live untested. Refused unless scripts/check.sh (HTML, links, web and mobile tests) passed
  on the commit that would go live, or on one with exactly the same files:
  - `gh pr create --base deploy` (release or revert PR): origin/<head>, head from --head or the
    current branch;
  - `gh pr merge` of a PR into deploy: the PR head (`--auto` refused);
  - `gh run rerun` of a run on deploy: the run's commit;
  - `gh workflow run` and `gh api` writes to this repository's /pages endpoints: origin/deploy.
  PR and run details come from `gh pr view` / `gh run view`: no answer = refused. Moving a PR onto
  deploy with `gh pr edit --base deploy` is always refused. check.sh appends "<commit> <tree> <time>"
  to <git common dir>/frs-check-passed after a passing run on a clean tree. Local origin/* refs are
  used, so fetch before testing (skill release does).

Shell commands from the Bash and PowerShell tools are tokenized with shlex (quotes and heredoc
bodies are respected) and the wrappers env, command, exec, nohup, time, eval and
`sh|bash -c STRING` are followed.

Human escape hatch: start Claude Code with FRS_ALLOW_PROTECTED=1 to disable the guard.
Exit code 2 = block (stderr is shown to Claude); 0 = allow. Python 3.8+, standard library only.
"""
import functools
import json
import os
import re
import shlex
import subprocess
import sys

PROTECTED = ("main", "deploy")
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
HINT = ("Work on your own branch in your own worktree, never a branch created in place: "
        "git worktree add -b <type>/<slug> .claude/worktrees/<slug> origin/main (skill start-task). "
        "The live site changes only through a release PR main -> deploy (skill release).")

# git subcommands that never write to the working tree, the index or a branch.
READ_ONLY_GIT = {
    "status", "diff", "log", "show", "rev-parse", "rev-list", "ls-files", "ls-tree", "ls-remote",
    "cat-file", "describe", "blame", "annotate", "grep", "shortlog", "merge-base", "name-rev",
    "for-each-ref", "show-ref", "show-branch", "cherry", "range-diff", "whatchanged",
    "check-ignore", "check-attr", "check-mailmap", "check-ref-format", "count-objects", "fsck",
    "verify-commit", "verify-tag", "var", "version", "help", "diff-tree", "diff-files", "diff-index",
}
# Options accepted next to `merge --ff-only` / `pull --ff-only` in a read-only checkout.
FF_ONLY_FLAGS = {"--ff-only", "-q", "--quiet", "-v", "--verbose", "--stat", "-n", "--no-stat",
                 "--progress", "--no-progress", "--prune", "-p", "--no-rebase"}
CONFIG_READ = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "--get-color",
               "--get-colorbool", "--list", "-l", "get", "list"}
CONFIG_WRITE = {"--unset", "--unset-all", "--add", "--replace-all", "--rename-section",
                "--remove-section", "-e", "--edit", "set", "unset", "rename-section",
                "remove-section", "edit"}

# Shell syntax.
OPERATOR_CHARS = ";&|\n()<>"
KEYWORDS = {"!", "{", "}", "if", "then", "else", "elif", "fi", "do", "done", "while", "until"}
CD_COMMANDS = {"cd", "pushd", "chdir", "set-location", "sl", "push-location"}
POSIX_SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
POWERSHELLS = {"pwsh", "powershell"}
HEREDOC = re.compile(r"(?<![<\\])<<(?!<)-?[ \t]*(['\"]?)([A-Za-z0-9_.-]+)\1")
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*", re.S)
NOT_LITERAL = "the path is not literal: $VAR, backticks, cd - or popd"
STAMP = "frs-check-passed"  # scripts/check.sh appends "<sha> <time>" here after a passing run
GH_API_VALUE_OPTS = ("-X", "--method", "-H", "--header", "-f", "--raw-field", "-F", "--field", "--input",
                     "-q", "--jq", "-t", "--template", "--hostname", "--cache", "-p", "--preview")
GH_API_BODY_OPTS = ("-f", "--raw-field", "-F", "--field", "--input")
GH_MERGE_VALUE_OPTS = ("-b", "--body", "-F", "--body-file", "-t", "--subject", "-R", "--repo",
                       "-A", "--author-email", "--match-head-commit")
GH_RERUN_VALUE_OPTS = ("-j", "--job", "-R", "--repo")


# --------------------------------------------------------------------------------------------
# Where does a command run?
# --------------------------------------------------------------------------------------------

def git(directory, *args):
    """Run git in `directory` and return its stripped stdout, or None on any failure."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE")}
    try:
        out = subprocess.run(["git", "-C", directory] + list(args), capture_output=True,
                             text=True, check=True, timeout=5, env=env)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip()


@functools.lru_cache(maxsize=None)
def repo_dirs(directory):
    """(git dir, common dir) of the checkout containing `directory`, as real paths, or None."""
    out = git(directory, "rev-parse", "--path-format=absolute", "--git-dir", "--git-common-dir")
    if out is None:  # git older than 2.31: paths come relative to `directory`
        out = git(directory, "rev-parse", "--git-dir", "--git-common-dir")
    lines = out.splitlines() if out else []
    if len(lines) != 2:
        return None
    return tuple(os.path.realpath(os.path.join(directory, line)) for line in lines)


@functools.lru_cache(maxsize=None)
def current_branch(directory):
    """Branch checked out in `directory`; '' when HEAD is detached or unknown."""
    return git(directory, "symbolic-ref", "--quiet", "--short", "HEAD") or ""


@functools.lru_cache(maxsize=None)
def project_common_dir():
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    dirs = repo_dirs(project) if project else None
    return dirs[1] if dirs else None


def in_project(dirs):
    """True if a checkout belongs to this repository (main checkout or any of its worktrees)."""
    ours = project_common_dir()
    return ours is None or dirs[1] == ours  # project unknown: treat every repository as ours


def existing_dir(path):
    directory = path if os.path.isdir(path) else os.path.dirname(path)
    while directory and not os.path.isdir(directory):
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent
    return directory or None


def classify(directory):
    """Return (kind, detail) for the directory a command runs in.

    kind is "outside" (not this repository), "main" (the main checkout; detail = its branch),
    "protected" (another checkout on main/deploy), "feature" (any other worktree) or
    "unknown" (detail = why the directory cannot be resolved).
    """
    if directory is None:
        return "unknown", NOT_LITERAL
    if not os.path.isdir(directory):
        ancestor = existing_dir(directory)
        dirs = repo_dirs(ancestor) if ancestor else None
        if dirs and in_project(dirs):
            return "unknown", "the directory does not exist yet"
        return "outside", ""
    dirs = repo_dirs(directory)
    if not dirs or not in_project(dirs):
        return "outside", ""
    branch = current_branch(directory)
    if dirs[0] == dirs[1]:
        return "main", branch
    if branch in PROTECTED:
        return "protected", branch
    return "feature", branch


def resolve(base, target):
    """Directory reached by `cd target` from `base`; None if it cannot be known here."""
    target = re.sub(r"^\$(\{HOME\}|HOME\b)", lambda _: os.path.expanduser("~"), target)
    if "$" in target or "`" in target:
        return None
    target = os.path.expanduser(target)
    if os.path.isabs(target):
        return os.path.normpath(target)
    return None if base is None else os.path.normpath(os.path.join(base, target))


# --------------------------------------------------------------------------------------------
# Shell parsing
# --------------------------------------------------------------------------------------------

def strip_heredoc_bodies(text):
    """Drop heredoc bodies: they are data (often commit messages), not commands."""
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for match in HEREDOC.finditer(line):
            end = i
            while end < len(lines) and lines[end].strip() != match.group(2):
                end += 1
            if end == len(lines):  # no terminator: keep the rest and analyze it
                return "\n".join(out + lines[i:])
            i = end + 1
    return "\n".join(out)


def strip_comments(text, escape):
    """Remove `# ...` shell comments (outside quotes, at the start of a word)."""
    out, quote, i = [], None, 0
    while i < len(text):
        c = text[i]
        if escape and c == "\\" and quote != "'" and i + 1 < len(text):
            out.append(text[i:i + 2])
            i += 2
            continue
        if quote:
            if c == quote:
                quote = None
        elif c in "'\"":
            quote = c
        elif c == "#" and (i == 0 or text[i - 1] in " \t\r\n;&|("):
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
            continue
        out.append(c)
        i += 1
    return "".join(out)


def tokenize(command, powershell=False):
    """Split a command line into words and operator tokens (`&&`, `;`, `(`, `>`, newline...)."""
    text = command if powershell else command.replace("\\\n", "")
    text = strip_comments(strip_heredoc_bodies(text), escape=not powershell)
    try:
        lexer = shlex.shlex(text, posix=True, punctuation_chars=OPERATOR_CHARS)
        lexer.whitespace = " \t\r"
        lexer.whitespace_split = True
        lexer.commenters = ""
        if powershell:
            lexer.escape = ""  # PowerShell escapes with a backtick; keep Windows backslashes
        return list(lexer)
    except ValueError:
        # Unbalanced quotes: fall back to a plain split on the shell operators.
        tokens = []
        for part in re.split(r"(&&|\|\||[;&|\n()])", text):
            if re.fullmatch(r"&&|\|\||[;&|\n()]", part):
                tokens.append(part)
                continue
            try:
                tokens.extend(shlex.split(part))
            except ValueError:
                tokens.extend(part.split())
        return tokens


def is_operator(token):
    return token != "" and all(c in OPERATOR_CHARS for c in token)


def command_name(word):
    name = re.split(r"[\\/]", word)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


def unwrap(words):
    """Strip what precedes the real command: NAME=value, shell keywords and the wrappers
    env/command/exec/nohup/time. Returns (words, assigned variable names, env -C target)."""
    names, chdir = set(), None
    while words:
        first, name = words[0], command_name(words[0])
        if ASSIGNMENT.fullmatch(first):
            names.add(first.split("=", 1)[0])
            words = words[1:]
        elif first in KEYWORDS:
            words = words[1:]
        elif name == "env":
            words = words[1:]
            while words:
                arg = words[0]
                if arg in ("-u", "--unset"):
                    words = words[2:]
                elif arg in ("-C", "--chdir") and len(words) > 1:
                    chdir, words = words[1], words[2:]
                elif arg.startswith("--chdir="):
                    chdir, words = arg.split("=", 1)[1], words[1:]
                elif arg in ("-S", "--split-string") and len(words) > 1:
                    try:
                        words = shlex.split(words[1]) + words[2:]
                    except ValueError:
                        words = words[1].split() + words[2:]
                elif arg.startswith("-"):
                    words = words[1:]
                elif ASSIGNMENT.fullmatch(arg):
                    names.add(arg.split("=", 1)[0])
                    words = words[1:]
                else:
                    break
        elif name == "command":
            words = words[1:]
            while words and words[0] in ("-p", "--"):
                words = words[1:]
            if words and words[0] in ("-v", "-V"):  # only looks the command up
                return [], names, chdir
        elif name == "exec":
            words = words[1:]
            while words and words[0].startswith("-"):
                words = words[2:] if words[0] == "-a" else words[1:]
        elif name in ("nohup", "time"):
            words = words[1:]
            while words and words[0] in ("-p", "--"):
                words = words[1:]
        else:
            break
    return words, names, chdir


def shell_string(words):
    """The STRING of `sh -c STRING` or `pwsh -Command STRING`, or None."""
    name, args = command_name(words[0]), words[1:]
    if name in POWERSHELLS:
        for k, arg in enumerate(args):
            if arg.lower() in ("-c", "-command"):
                return " ".join(args[k + 1:])
        return None
    has_c = False
    while args:
        arg = args[0]
        if arg in ("-o", "+o", "-O", "+O"):
            args = args[2:]
        elif arg in ("--", "-"):
            args = args[1:]
            break
        elif arg.startswith("--"):
            args = args[1:]
        elif re.fullmatch(r"[-+][A-Za-z]+", arg):
            has_c = has_c or (arg[0] == "-" and "c" in arg)
            args = args[1:]
        else:
            break
    return args[0] if has_c and args else None


def git_invocations(command, base, powershell=False, depth=0):
    """Yield (directory, argv) for each git or gh command in a shell command line, following cd.

    argv starts with "git" or "gh", followed by the subcommand and its arguments.

    `directory` is None when it cannot be known here ($VAR or backticks in cd / -C / env -C).
    """
    if depth > 5:
        return
    stack, words = [], []
    tokens = tokenize(command, powershell) + [";"]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        i += 1
        if not is_operator(token):
            words.append(token)
            continue
        if ("<" in token or ">" in token) and not token.endswith("("):
            # Redirection: drop the operator, its target and a file descriptor number before it.
            if words and words[-1].isdigit():
                words.pop()
            i += 1
            continue
        if words:
            base = yield from simple_command(words, base, powershell, depth)
            words = []
        for char in token:  # subshells: a cd inside ( ... ) does not outlive it
            if char == "(":
                stack.append(base)
            elif char == ")" and stack:
                base = stack.pop()


def simple_command(words, base, powershell, depth):
    """Yield the git invocations of one simple command; return the directory after it."""
    words, names, chdir = unwrap(words)
    if not words:
        return base
    name = command_name(words[0])
    if name in CD_COMMANDS:
        args = [a for a in words[1:] if a == "-" or not a.startswith("-")]
        if not args:
            return os.path.expanduser("~") if name in ("cd", "chdir") else None
        return None if args[0] == "-" else resolve(base, args[0])
    if name in ("popd", "pop-location"):
        return None
    here = base if chdir is None else resolve(base, chdir)
    if name in POSIX_SHELLS or name in POWERSHELLS:
        inner = shell_string(words)
        if inner is not None:
            yield from git_invocations(inner, here, name in POWERSHELLS, depth + 1)
        return base
    if name == "eval":
        yield from git_invocations(" ".join(words[1:]), here, powershell, depth + 1)
        return base
    if name == "gh":
        if len(words) > 1:
            yield here, ["gh"] + words[1:]
        return base
    if name != "git":
        return base
    if names & {"GIT_DIR", "GIT_WORK_TREE"}:
        here = None
    args = words[1:]
    while args and args[0].startswith("-"):  # git's own options, before the subcommand
        opt = args[0]
        if opt == "-C" and len(args) > 1:
            here, args = resolve(here, args[1]), args[2:]
        elif opt in ("--git-dir", "--work-tree"):
            here, args = None, args[2:]
        elif opt.startswith(("--git-dir=", "--work-tree=")):
            here, args = None, args[1:]
        elif opt in ("-c", "--namespace", "--config-env", "--super-prefix", "--attr-source"):
            args = args[2:]
        else:
            args = args[1:]
    if args:
        yield here, ["git"] + args
    return base


# --------------------------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------------------------

def short_branch(ref):
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def split_args(rest, value_opts=()):
    """(options, positionals) of a subcommand; options in `value_opts` swallow the next word."""
    options, positionals, k = [], [], 0
    while k < len(rest):
        arg = rest[k]
        k += 1
        if arg == "--":
            positionals.extend(rest[k:])
            break
        if arg.startswith("-") and len(arg) > 1:
            options.append(arg)
            if arg in value_opts and k < len(rest):
                k += 1
        else:
            positionals.append(arg)
    return options, positionals


def unknown_dir_message(sub, reason):
    fix = ("Run it in a separate call once the directory exists." if "exist" in reason
           else "Repeat the command with a literal absolute path in cd / git -C.")
    return (f"Cannot tell which checkout 'git {sub}' would run in ({reason}). Only read-only git, "
            "fetch, worktree add/remove, branch -d and merge --ff-only origin/main are accepted "
            f"there. {fix}")


def push_destinations(directory):
    """Branches a ref-less `git push` from `directory` could update."""
    found = {current_branch(directory)}
    target = git(directory, "rev-parse", "--symbolic-full-name", "@{push}") or ""
    if target.startswith("refs/remotes/") and target.count("/") >= 3:
        found.add(target.split("/", 3)[3])
    return found - {""}


def check_push(directory, rest):
    positionals, repo_given, tags = [], False, False
    k = 0
    while k < len(rest):
        arg = rest[k]
        k += 1
        if arg == "--":
            positionals.extend(rest[k:])
            break
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            if name.startswith("--force"):
                return f"Force push refused: git push {' '.join(rest)}"
            if name in ("--delete", "--prune"):
                return f"Push that deletes remote branches refused: git push {' '.join(rest)}"
            if name in ("--all", "--branches", "--mirror"):
                return f"'git push {name}' refused: it pushes every branch, main and deploy included."
            repo_given = repo_given or name == "--repo"
            tags = tags or name == "--tags"
            if "=" not in arg and name in ("--push-option", "--repo", "--receive-pack", "--exec"):
                k += 1
            continue
        if arg.startswith("-o"):
            k += 1 if arg == "-o" else 0
            continue
        if re.fullmatch(r"-[A-Za-z0-9]+", arg):
            if "f" in arg:
                return f"Force push refused: git push {' '.join(rest)}"
            if "d" in arg:
                return f"Push that deletes remote branches refused: git push {' '.join(rest)}"
            continue
        positionals.append(arg)
    refspecs = positionals if repo_given else positionals[1:]
    for spec in refspecs:
        if spec.startswith("+"):
            return f"Force push refused (refspec '{spec}')."
        if "*" in spec:
            return f"Push with a wildcard refspec refused ('{spec}')."
        src, colon, dst = spec.partition(":")
        if colon and not src:
            return f"Push that deletes or matches remote branches refused (refspec '{spec}')."
        dest = dst or src
        if dest in ("HEAD", "@"):
            if directory is None:
                return unknown_dir_message("push", NOT_LITERAL)
            dest = current_branch(directory) or dest
        if short_branch(dest) in PROTECTED:
            return f"Push to protected branch '{short_branch(dest)}' refused."
    if not refspecs and not tags:
        if directory is None:
            return unknown_dir_message("push", NOT_LITERAL)
        for dest in push_destinations(directory):
            if dest in PROTECTED:
                return f"Push without a refspec would update '{dest}': refused."
    return None


def checkout_target(sub, rest, directory):
    """Branch that `git checkout|switch` would put HEAD on (or create), else None."""
    created, detach, paths, positionals = None, False, False, []
    k = 0
    while k < len(rest):
        arg = rest[k]
        k += 1
        if arg == "--":
            paths = True
            break
        if arg in ("-b", "-B", "-c", "-C", "--orphan") and k < len(rest):
            created = rest[k]
            k += 1
        elif arg == "--detach" or (sub == "switch" and arg == "-d"):
            detach = True
        elif not arg.startswith("-") or arg == "-":
            positionals.append(arg)
    if created is not None:
        return created
    if detach or paths or len(positionals) != 1:
        return None  # detached HEAD or a file checkout: no branch is switched to
    target = positionals[0]
    if (target == "-" or target.startswith("@{-")) and directory is not None:
        target = git(directory, "rev-parse", "--abbrev-ref", "@{-1}" if target == "-" else target) or target
    return target


def worktree_add_branch(rest):
    """Branch a new worktree would check out or create, or None for --detach."""
    new_branch, detach, positionals = None, False, []
    k = 1  # rest[0] == "add"
    while k < len(rest):
        arg = rest[k]
        k += 1
        if arg in ("-b", "-B") and k < len(rest):
            new_branch = rest[k]
            k += 1
        elif arg == "--reason":
            k += 1
        elif arg in ("-d", "--detach"):
            detach = True
        elif arg == "--":
            positionals.extend(rest[k:])
            break
        elif not arg.startswith("-"):
            positionals.append(arg)
    if new_branch or detach:
        return new_branch
    if len(positionals) >= 2:
        return positionals[1]
    # `git worktree add <path>` uses (or creates) the branch named after the last path component.
    return os.path.basename(positionals[0].rstrip("/\\")) if positionals else None


def branch_mode(rest):
    """Classify `git branch` arguments: (mode, positionals), mode in
    list | delete | move | upstream | create."""
    value_opts = {"--contains", "--no-contains", "--merged", "--no-merged", "--points-at",
                  "--sort", "--format", "--set-upstream-to", "-u"}
    letters, longs, positionals, k = set(), set(), [], 0
    while k < len(rest):
        arg = rest[k]
        k += 1
        if arg == "--":
            positionals.extend(rest[k:])
            break
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            longs.add(name)
            if "=" not in arg and name in value_opts and k < len(rest) and not rest[k].startswith("-"):
                k += 1
        elif arg.startswith("-") and len(arg) > 1:
            letters.update(arg[1:])
            if arg.endswith("u") and k < len(rest):
                k += 1
        else:
            positionals.append(arg)
    if letters & set("dD") or "--delete" in longs:
        return "delete", positionals
    if letters & set("mMcC") or longs & {"--move", "--copy"}:
        return "move", positionals
    if "u" in letters or longs & {"--set-upstream-to", "--unset-upstream", "--edit-description"}:
        return "upstream", positionals
    if (not positionals or letters & set("larv")
            or longs & {"--list", "--all", "--remotes", "--show-current", "--contains",
                        "--no-contains", "--merged", "--no-merged", "--points-at", "--verbose"}):
        return "list", positionals
    return "create", positionals


def protected_ref_change(sub, rest, directory):
    """Rules valid in every checkout of this repository: main and deploy are never switched to,
    checked out in a worktree, renamed, deleted, moved or overwritten by a fetch."""
    if sub in ("checkout", "switch"):
        target = checkout_target(sub, rest, directory)
        if target is not None and short_branch(target) in PROTECTED:
            return (f"'git {sub}' to '{short_branch(target)}' refused: agents never switch a "
                    f"checkout to a protected branch. To look at it: "
                    f"git worktree add --detach <path> origin/{short_branch(target)}")
    elif sub == "worktree" and rest[:1] == ["add"]:
        target = worktree_add_branch(rest)
        if target is not None and short_branch(target) in PROTECTED:
            return (f"A worktree on protected branch '{short_branch(target)}' refused: use "
                    f"git worktree add --detach <path> origin/{short_branch(target)}")
    elif sub == "branch":
        mode, positionals = branch_mode(rest)
        names = positionals if mode in ("delete", "move") else positionals[:1] if mode == "create" else []
        for name in names:
            if short_branch(name) in PROTECTED:
                return f"'git branch' on protected branch '{short_branch(name)}' refused."
    elif sub == "update-ref":
        _, positionals = split_args(rest, value_opts=("-m",))
        if positionals and short_branch(positionals[0]) in PROTECTED:
            return f"'git update-ref' on protected branch '{short_branch(positionals[0])}' refused."
    elif sub in ("fetch", "pull"):
        _, positionals = split_args(rest, value_opts=("--upload-pack", "--depth", "-j", "--jobs"))
        for spec in positionals[1:]:
            dst = spec.lstrip("+").partition(":")[2]
            if short_branch(dst) in PROTECTED:
                return f"'git {sub}' into the local '{short_branch(dst)}' branch refused."
    return None


def read_only_allowed(sub, rest, branch):
    """True if `git sub rest` is acceptable in a read-only checkout."""
    options, positionals = split_args(rest)
    if sub in READ_ONLY_GIT:
        return not any(o.startswith("--output") for o in options)
    if sub == "fetch":
        return not any(o == "-u" or o.startswith(("--update-head-ok", "--upload-pack"))
                       for o in options)
    if sub == "worktree":
        return positionals[:1] in (["add"], ["remove"], ["prune"], ["list"])
    if sub == "branch":  # listing, or a safe delete (-d): never -D / --force
        mode = branch_mode(rest)[0]
        forced = any(a == "--force" or (a.startswith("-") and not a.startswith("--") and "D" in a)
                     for a in rest)
        return mode == "list" or (mode == "delete" and not forced)
    if sub in ("merge", "pull"):
        if "--ff-only" not in options or not set(options) <= FF_ONLY_FLAGS:
            return False
        if sub == "pull":  # git pull --ff-only [origin [<current branch>]]
            return positionals in ([], ["origin"]) or (bool(branch) and positionals == ["origin", branch])
        sources = {"origin/main", "refs/remotes/origin/main", "@{u}", "@{upstream}"}
        if branch:
            sources |= {"origin/" + branch, "refs/remotes/origin/" + branch}
        return len(positionals) <= 1 and set(positionals) <= sources
    if sub == "config":
        return (any(a in CONFIG_READ for a in rest)
                or (len(positionals) == 1 and not any(a in CONFIG_WRITE for a in rest)))
    if sub == "remote":
        return not positionals or positionals[0] in ("show", "get-url", "prune", "update")
    if sub == "tag":
        return not positionals or any(
            o in ("-l", "--list", "-v", "--verify")
            or o.startswith(("--contains", "--no-contains", "--points-at", "--merged", "--no-merged"))
            for o in options)
    if sub == "stash":
        return positionals[:1] in (["list"], ["show"])
    if sub == "reflog":
        return positionals[:1] not in (["expire"], ["delete"], ["drop"])
    if sub == "symbolic-ref":
        return len(positionals) <= 1 and not any(o in ("-d", "--delete") for o in options)
    return False


def check_git(directory, args):
    """Return a refusal message for one git invocation, or None to allow it."""
    sub, rest = args[0], args[1:]
    if sub == "push":  # push rules hold in any repository
        return check_push(directory, rest)
    kind, detail = classify(directory)
    if kind == "outside":
        return None
    problem = protected_ref_change(sub, rest, directory)
    if problem or kind == "feature":
        return problem
    if read_only_allowed(sub, rest, detail if kind != "unknown" else ""):
        return None
    if kind == "unknown":
        return unknown_dir_message(sub, detail)
    if kind == "main":
        state = f"on branch '{detail}'" if detail else "on a detached HEAD"
        message = f"'git {sub}' refused: the main checkout ({state}) is read-only for agents."
        if sub in ("checkout", "switch"):
            message += " Do not create or switch branches in place."
        return message
    return f"'git {sub}' refused: the checkout on protected branch '{detail}' is read-only."


def tested(ref):
    """True if scripts/check.sh passed on the commit `ref` (a ref or a full sha) points to, or on a
    commit with the same tree: a release merge commit has the files of the main it merges (see STAMP)."""
    common = project_common_dir()
    if common is None:
        return True  # outside this project: nothing to enforce
    sha = git(common, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    tree = git(common, "rev-parse", "--verify", "--quiet", ref + "^{tree}")
    if not sha or not tree:
        return False
    try:
        with open(os.path.join(common, STAMP)) as stamps:
            return any(line.split()[:1] == [sha] or line.split()[1:2] == [tree] for line in stamps)
    except OSError:
        return False


def option_value(args, short, long):
    """Value of an option written `-X v`, `-Xv`, `--long v` or `--long=v`; None if absent."""
    for k, arg in enumerate(args):
        if arg in (short, long):
            return args[k + 1] if k + 1 < len(args) else ""
        if arg.startswith(long + "="):
            return arg[len(long) + 1:]
        if not arg.startswith("--") and arg.startswith(short) and len(arg) > len(short):
            return arg[len(short):]
    return None


def gh_fields(directory, command):
    """Whitespace-separated output of a read-only gh command, or None if gh cannot answer."""
    try:
        out = subprocess.run(command, capture_output=True, text=True, check=True, timeout=7,
                             cwd=directory if directory and os.path.isdir(directory) else None)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.split()


def untested(what):
    return (f"publishing refused: scripts/check.sh (HTML, links, web and mobile tests) has not passed on "
            f"{what}. Fetch, run it on a clean checkout of that commit (skill release, step 3), then retry.")


def check_gh(directory, args):
    """Return a refusal message when a gh command publishes something untested, or None."""
    repo = option_value(args[2:], "-R", "--repo")
    repo_args = ["--repo", repo] if repo else []
    if args[:2] == ["pr", "edit"]:
        if short_branch(option_value(args, "-B", "--base") or "") == "deploy":
            return ("'gh pr edit --base deploy' refused: only a release PR from main (skill release) or a "
                    "revert PR goes into deploy, opened with gh pr create after the tests.")
        return None
    if args[:2] == ["pr", "create"]:
        if short_branch(option_value(args, "-B", "--base") or "") != "deploy":
            return None
        head = option_value(args, "-H", "--head") or (current_branch(directory) if directory else "")
        head = short_branch(head.split(":", 1)[-1])
        if not head:
            return "'gh pr create --base deploy' refused: cannot tell the head branch. Pass --head <branch>."
        return None if tested("refs/remotes/origin/" + head) else untested(f"origin/{head}")
    if args[:2] == ["pr", "merge"]:
        _, positionals = split_args(args[2:], value_opts=GH_MERGE_VALUE_OPTS)
        fields = gh_fields(directory, ["gh", "pr", "view"] + positionals[:1] + repo_args
                           + ["--json", "baseRefName,headRefOid", "--jq", '.baseRefName + " " + .headRefOid'])
        if not fields or len(fields) != 2:
            return ("'gh pr merge' refused: cannot tell (via gh pr view) whether the PR goes into deploy, "
                    "the live site. Check the PR with gh pr view, then retry.")
        base, head = fields
        if short_branch(base) != "deploy":
            return None
        if "--auto" in args:
            return ("'gh pr merge --auto' into deploy refused: a later commit could go live untested. "
                    "Test the PR head, then merge it directly.")
        return None if tested(head) else untested(f"{head[:12]}, the head of this PR into deploy")
    if args[:2] == ["run", "rerun"]:
        _, positionals = split_args(args[2:], value_opts=GH_RERUN_VALUE_OPTS)
        if not positionals:
            return "'gh run rerun' refused without a run id: pass it, so the guard can check what it deploys."
        fields = gh_fields(directory, ["gh", "run", "view", positionals[0]] + repo_args
                           + ["--json", "headBranch,headSha", "--jq", '.headBranch + " " + .headSha'])
        if not fields or len(fields) != 2:
            return ("'gh run rerun' refused: cannot tell (via gh run view) whether the run deploys the live "
                    "site. Check the run with gh run view, then retry.")
        branch, sha = fields
        if branch != "deploy":
            return None
        return None if tested(sha) else untested(f"{sha[:12]}, the commit of this run on deploy")
    if args[:2] == ["workflow", "run"]:
        return None if tested("refs/remotes/origin/deploy") else untested("origin/deploy")
    if args[:1] == ["api"]:
        options, positionals = split_args(args[1:], value_opts=GH_API_VALUE_OPTS)
        method = (option_value(args, "-X", "--method") or "").upper()
        if not method:
            body = any(o in GH_API_BODY_OPTS or o.startswith(("--raw-field=", "--field=", "--input="))
                       for o in options)
            method = "POST" if body else "GET"
        endpoint = positionals[0].lower() if positionals else ""
        if method == "GET" or not re.search(r"(^|/)pages(/|$)", endpoint):
            return None
        ours = ("fosteringresearchsynergies.github.io" in endpoint
                or ("{repo}" in endpoint and classify(directory)[0] != "outside"))
        if not ours:
            return None  # another repository (e.g. frs-workshop-redirect)
        return None if tested("refs/remotes/origin/deploy") else untested("origin/deploy")
    return None


# --------------------------------------------------------------------------------------------
# Entry points
# --------------------------------------------------------------------------------------------

def block(message, hint=True):
    print(f"[guard] {message}" + (f"\n{HINT}" if hint else ""), file=sys.stderr)
    return 2


def check_edit(tool_input):
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return 0
    path = os.path.abspath(os.path.expanduser(path))
    directory = existing_dir(path)
    kind, branch = classify(directory) if directory else ("outside", "")
    if kind == "main":
        state = f"on branch '{branch}'" if branch else "on a detached HEAD"
        return block(f"{path} is in the main checkout ({state}), which is read-only for agents.")
    if kind == "protected":
        return block(f"{path} is in a checkout on protected branch '{branch}'.")
    return 0


def check_shell(tool_input, session_cwd, powershell):
    command = tool_input.get("command") or ""
    for directory, argv in git_invocations(command, session_cwd or os.getcwd(), powershell):
        if argv[0] == "gh":
            problem = check_gh(directory, argv[1:])
            if problem:
                return block(problem, hint=False)
        else:
            problem = check_git(directory, argv[1:])
            if problem:
                return block(problem)
    return 0


def main():
    if os.environ.get("FRS_ALLOW_PROTECTED") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("payload is not a JSON object")
        tool = payload.get("tool_name")
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            raise ValueError("tool_input is not a JSON object")
    except ValueError as exc:  # unreadable input: fail closed like any other error
        return block(f"unreadable hook input ({exc}). "
                     "A human can bypass the guard with FRS_ALLOW_PROTECTED=1.")
    try:
        if tool in EDIT_TOOLS:
            return check_edit(tool_input)
        if tool in SHELL_TOOLS:
            return check_shell(tool_input, payload.get("cwd"), tool == "PowerShell")
    except Exception as exc:  # a bug here must not open the gate: fail closed, say why
        return block(f"internal error in the guard ({type(exc).__name__}: {exc}). "
                     "Report it; a human can bypass the guard with FRS_ALLOW_PROTECTED=1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

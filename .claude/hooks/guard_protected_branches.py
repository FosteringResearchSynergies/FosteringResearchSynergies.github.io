#!/usr/bin/env python3
"""PreToolUse guard: keep agents off the protected branches.

- Blocks Edit/Write/NotebookEdit on files whose checkout is on `main` or `deploy`.
- Blocks `git commit`/`merge`/`pull`/`rebase`/`cherry-pick`/`am`/`revert`/`reset --hard`
  run in a checkout that is on a protected branch (except `merge`/`pull --ff-only`, used to sync).
- Blocks `git push` that targets a protected branch or uses --force/-f/--mirror/--delete.

Agents must work on a short-lived branch in their own worktree
(see .claude/skills/start-task). Human escape hatch: FRS_ALLOW_PROTECTED=1.
Exit code 2 = block (stderr is shown to Claude); anything else = allow.
"""
import json
import os
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "deploy"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
GUARDED_GIT = {"commit", "merge", "pull", "rebase", "cherry-pick", "am", "revert", "reset"}
HINT = "Create a branch + worktree first (skill: start-task); deploy only via a release PR main -> deploy (skill: release)."


def git(directory, *args):
    try:
        out = subprocess.run(["git", "-C", directory, *args], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return None
    return out.stdout.strip()


def existing_dir(path):
    directory = path if os.path.isdir(path) else os.path.dirname(path)
    while directory and not os.path.isdir(directory):
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent
    return directory or None


def same_project(directory):
    """True if `directory` belongs to this project's repository (main checkout or any worktree)."""
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project:
        return True
    ours = git(project, "rev-parse", "--path-format=absolute", "--git-common-dir")
    theirs = git(directory, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return bool(ours and theirs and os.path.realpath(ours) == os.path.realpath(theirs))


def protected_branch(directory):
    if not directory or not same_project(directory):
        return None
    branch = git(directory, "rev-parse", "--abbrev-ref", "HEAD")
    return branch if branch in PROTECTED else None


def block(message):
    print(f"[guard] {message}\n{HINT}", file=sys.stderr)
    return 2


def check_edit(tool_input):
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return 0
    branch = protected_branch(existing_dir(os.path.abspath(path)))
    if branch:
        return block(f"{path} is in a checkout on protected branch '{branch}'.")
    return 0


def git_invocations(command, base):
    """Yield (directory, args) for each `git ...` segment of a shell command, following `cd`."""
    for segment in re.split(r"&&|\|\||;|\||\n", command):
        segment = re.sub(r"[()]", " ", segment)
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        while words and re.fullmatch(r"\w+=.*", words[0]):
            words = words[1:]
        if not words:
            continue
        if words[0] == "cd" and len(words) > 1:
            base = os.path.join(base, os.path.expanduser(words[1]))
            continue
        if os.path.basename(words[0]) != "git":
            continue
        words, directory = words[1:], base
        while words and words[0].startswith("-"):
            if words[0] == "-C" and len(words) > 1:
                directory, words = os.path.join(directory, os.path.expanduser(words[1])), words[2:]
            elif words[0] in ("-c", "--git-dir", "--work-tree") and len(words) > 1:
                words = words[2:]
            else:
                words = words[1:]
        if words:
            yield directory, words


def check_bash(tool_input, session_cwd):
    command = tool_input.get("command") or ""
    for directory, args in git_invocations(command, session_cwd or os.getcwd()):
        sub, rest = args[0], args[1:]
        if sub == "push":
            if any(a in ("--force", "-f", "--mirror", "--delete", "-d") or a.startswith("--force") for a in rest):
                return block(f"Destructive push refused: git {' '.join(args)}")
            refs = [a for a in rest if not a.startswith("-")][1:]
            for ref in refs:
                dest = ref.split(":")[-1].removeprefix("+").removeprefix("refs/heads/")
                if dest in PROTECTED:
                    return block(f"Direct push to protected branch '{dest}' refused.")
            if not refs and protected_branch(directory):
                return block("Push from a checkout on a protected branch refused.")
            continue
        if sub in ("merge", "pull") and "--ff-only" in rest:
            continue
        if sub == "reset" and "--hard" not in rest:
            continue
        if sub in GUARDED_GIT:
            branch = protected_branch(directory)
            if branch:
                return block(f"'git {sub}' on protected branch '{branch}' refused.")
    return 0


def main():
    if os.environ.get("FRS_ALLOW_PROTECTED") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if tool in EDIT_TOOLS:
        return check_edit(tool_input)
    if tool == "Bash":
        return check_bash(tool_input, payload.get("cwd"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

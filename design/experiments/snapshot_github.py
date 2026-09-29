#!/usr/bin/env python3
"""Take the GitHub snapshot the design experiments read - once - and keep it.

The experiments must build offline and give the same bytes twice, so the
network is read here and nowhere else:

  * every repository on the account: name, visibility, creation date,
    description, URL;
  * for the repositories NOT cloned on this machine: every commit's date and
    whether it carries a Claude or Gemini Co-Authored-By trailer, and whether
    the files the ledger column asks about exist at the default branch.

The file is named for the day it was taken, and build.py names the file it
reads, so a new snapshot is a deliberate change of source rather than a
silent one.

    python snapshot_github.py      # writes sources/github-<today>.json
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OWNER = "loganw234"
NOT_CLONED = ["CanonBracketTool", "Microscope-Stacker"]
ASKED_FILES = ["docs/VALIDATION.md", "CLAUDE.md"]
AGENT = re.compile(r"^Co-Authored-By:.*\b(claude|gemini)\b", re.I | re.M)


def gh(*args, allow_404=False):
    r = subprocess.run(["gh", *args], capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        if allow_404 and '"status":"404"' in out.replace(" ", ""):
            return None
        sys.exit("gh %s failed (%d): %s" % (" ".join(args), r.returncode,
                                            r.stderr.decode("utf-8", "replace").strip() or out[:200]))
    return out


def main():
    repos = json.loads(gh("repo", "list", OWNER, "--limit", "500", "--json",
                          "name,visibility,createdAt,description,url"))
    if len(repos) >= 500:
        sys.exit("the account lists 500 or more repositories; raise --limit, "
                 "or this snapshot is silently partial")
    # Published with the site's repository: every public repository, and a
    # private one only if the experiments read it (added before the first commit).
    sys.path.insert(0, str(HERE))
    from build import PINS
    reads = set(PINS) | set(NOT_CLONED)
    repos = [r for r in repos if r["visibility"] == "PUBLIC" or r["name"] in reads]

    commits = {}
    for name in NOT_CLONED:
        lines = gh("api", "--paginate", "repos/%s/%s/commits?per_page=100" % (OWNER, name),
                   "--jq", ".[] | {date: .commit.author.date, message: .commit.message} | @json")
        recs = [json.loads(json.loads(l)) if l.startswith('"') else json.loads(l)
                for l in lines.splitlines() if l.strip()]
        if not recs:
            sys.exit("%s: the API returned no commits" % name)
        files = {}
        for path in ASKED_FILES:
            files[path] = gh("api", "repos/%s/%s/contents/%s" % (OWNER, name, path),
                             "--jq", ".name", allow_404=True) is not None
        commits[name] = {
            "total": len(recs),
            "agent_coauthored": sum(1 for c in recs if AGENT.search(c["message"])),
            "first": min(c["date"] for c in recs)[:10],
            "files": files,
        }

    now = datetime.datetime.now().astimezone()
    snap = {
        "taken": now.isoformat(timespec="seconds"),
        "owner": OWNER,
        "command": "python snapshot_github.py (gh repo list + gh api, see its docstring)",
        "repos": sorted(repos, key=lambda r: r["name"].lower()),
        "not_cloned": commits,
    }
    out = HERE / "sources" / ("github-%s.json" % now.date().isoformat())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print("wrote %s: %d repositories, %d not cloned here" % (out.relative_to(HERE), len(repos), len(commits)))


if __name__ == "__main__":
    main()

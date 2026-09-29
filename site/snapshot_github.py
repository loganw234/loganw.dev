#!/usr/bin/env python3
"""Take the GitHub snapshot the site reads - once per snapshot - and keep it.

The build must be offline and give the same bytes twice, so the network is
read here and nowhere else. What it records, all through `gh`:

  * every repository on the account: name, visibility, creation date,
    description, URL, and whether it is a fork;
  * for each repository pins.json lists under "github_only" (not cloned on
    the build machine): every commit's date and whether it carries a Claude
    or Gemini Co-Authored-By trailer, and whether the ledger and agent-notes
    files exist on its default branch;
  * for each pinned repository that declares CI workflows under
    "verified_by": every run of those workflows - its commit, conclusion,
    date and URL - which is what "last verified" is computed from.

The file is named for the day it was taken, and pins.json names the file the
build reads, so taking a new snapshot is a deliberate change of source.

    python site/snapshot_github.py      # writes sources/github-<today>.json
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PINS = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
OWNER = PINS["owner"]
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


def lines_json(out):
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def main():
    repos = json.loads(gh("repo", "list", OWNER, "--limit", "500", "--json",
                          "name,visibility,createdAt,description,url,isFork"))
    if len(repos) >= 500:
        sys.exit("the account lists 500 or more repositories; raise --limit, "
                 "or this snapshot is silently partial")
    names = {r["name"] for r in repos}
    # This file is published. It records every public repository, which is
    # public anyway, and a private one only if the site reads it. The first
    # snapshot recorded every private repository on the account, and was
    # filtered before the first commit.
    reads = set(PINS["repos"]) | set(PINS["github_only"])
    repos = [r for r in repos if r["visibility"] == "PUBLIC" or r["name"] in reads]

    github_only = {}
    for name in PINS["github_only"]:
        if name not in names:
            sys.exit("pins.json lists %s under github_only, and the account has no such repository" % name)
        recs = lines_json(gh("api", "--paginate", "repos/%s/%s/commits?per_page=100" % (OWNER, name),
                             "--jq", ".[] | {date: .commit.author.date, message: .commit.message}"))
        if not recs:
            sys.exit("%s: the API returned no commits" % name)
        files = {}
        for path in ASKED_FILES:
            files[path] = gh("api", "repos/%s/%s/contents/%s" % (OWNER, name, path),
                             "--jq", ".name", allow_404=True) is not None
        github_only[name] = {
            "total": len(recs),
            "agent_coauthored": sum(1 for c in recs if AGENT.search(c["message"])),
            "first": min(c["date"] for c in recs)[:10],
            "files": files,
        }

    runs = {}
    for name, cfg in sorted(PINS["repos"].items()):
        wanted = cfg.get("verified_by", {}).get("ci", [])
        if not wanted:
            continue
        got = lines_json(gh("api", "--paginate", "repos/%s/%s/actions/runs?per_page=100" % (OWNER, name),
                            "--jq", ".workflow_runs[] | {workflow: .name, sha: .head_sha, branch: .head_branch, "
                                    "status: .status, conclusion: .conclusion, created: .created_at, url: .html_url}"))
        mine = [r for r in got if r["workflow"] in wanted]
        missing = set(wanted) - {r["workflow"] for r in mine}
        if missing:
            sys.exit("%s: pins.json declares CI workflow(s) %s, which never ran" % (name, sorted(missing)))
        runs[name] = sorted(mine, key=lambda r: (r["created"], r["sha"]))

    now = datetime.datetime.now().astimezone()
    snap = {
        "taken": now.isoformat(timespec="seconds"),
        "owner": OWNER,
        "command": "python site/snapshot_github.py (gh repo list and gh api; see its docstring)",
        "repos": sorted(repos, key=lambda r: r["name"].lower()),
        "github_only": github_only,
        "runs": runs,
    }
    out = ROOT / "sources" / ("github-%s.json" % now.date().isoformat())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print("wrote %s: %d repositories, %d read through the API only, CI runs for %s"
          % (out.relative_to(ROOT).as_posix(), len(repos), len(github_only),
             ", ".join("%s (%d)" % (k, len(v)) for k, v in runs.items())))


if __name__ == "__main__":
    main()

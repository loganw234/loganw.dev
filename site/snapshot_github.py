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
  * for every pinned repository, the full SHA GitHub gives for its pin, or
    null where GitHub does not have that commit (the build refuses such a
    pin, and a pin this snapshot did not look up);
  * for every pinned repository, the name of every GitHub Actions workflow
    it has, which pins.json must class, one by one;
  * for every workflow pins.json classes as "verifies": every run - its
    commit, conclusion, date and URL - which is what "last verified" is
    computed from. A verifying workflow that never ran simply has no runs;
    the build then finds no pass, and says so.

A repository key is 'owner/name' where the owner is not pins.json's own
(the Mercenaries-Fan-Build organisation's repositories, for the Preservation
thread's credits); each owner the keys name is listed.

The file is named for the minute it was taken, is never overwritten, and
pins.json names the file the build reads, so taking a new snapshot is a
deliberate change of source.

    python site/snapshot_github.py      # writes sources/github-<date>-<HHMM>.json
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site"))
from facts import agent_credited          # noqa: E402  the one rule, shared with facts.agents

PINS = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
OWNER = PINS["owner"]
ASKED_FILES = ["docs/VALIDATION.md", "CLAUDE.md"]


def gh(*args, allow_404=False, allow_missing=False):
    """allow_404: a missing file is None. allow_missing: a commit GitHub does
    not have (404, or 422 for a SHA it cannot resolve) is None."""
    r = subprocess.run(["gh", *args], capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        status = re.search(r'"status":"(\d+)"', out.replace(" ", ""))
        code = status.group(1) if status else ""
        if (code == "404" and (allow_404 or allow_missing)) or (code == "422" and allow_missing):
            return None
        sys.exit("gh %s failed (%d): %s" % (" ".join(args), r.returncode,
                                            r.stderr.decode("utf-8", "replace").strip() or out[:200]))
    return out


def lines_json(out):
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def full(key):
    """'owner/name' for a key; a bare key is the default owner's."""
    return key if "/" in key else "%s/%s" % (OWNER, key)


def main():
    keys = list(PINS["repos"]) + list(PINS["github_only"])
    owners = sorted({full(k).split("/")[0] for k in keys})
    repos = []
    for owner in owners:
        got = json.loads(gh("repo", "list", owner, "--limit", "500", "--json",
                            "name,visibility,createdAt,description,url,isFork"))
        if len(got) >= 500:
            sys.exit("%s lists 500 or more repositories; raise --limit, "
                     "or this snapshot is silently partial" % owner)
        repos += [dict(r, owner=owner) for r in got]
    names = {"%s/%s" % (r["owner"], r["name"]) for r in repos}
    # This file is published. It records every public repository, which is
    # public anyway, and a private one only if the site reads it. The first
    # snapshot recorded every private repository on the account, and was
    # filtered before the first commit.
    reads = {full(k) for k in keys}
    repos = [r for r in repos if r["visibility"] == "PUBLIC" or "%s/%s" % (r["owner"], r["name"]) in reads]

    github_only = {}
    for name in PINS["github_only"]:
        if full(name) not in names:
            sys.exit("pins.json lists %s under github_only, and no such repository exists" % name)
        recs = lines_json(gh("api", "--paginate", "repos/%s/commits?per_page=100" % full(name),
                             "--jq", ".[] | {date: .commit.author.date, message: .commit.message}"))
        if not recs:
            sys.exit("%s: the API returned no commits" % name)
        files = {}
        for path in ASKED_FILES:
            files[path] = gh("api", "repos/%s/contents/%s" % (full(name), path),
                             "--jq", ".name", allow_404=True) is not None
        github_only[name] = {
            "total": len(recs),
            "agent_coauthored": sum(1 for c in recs if agent_credited(c["message"])),
            "first": min(c["date"] for c in recs)[:10],
            "files": files,
        }

    # Every pin, as GitHub resolves it. A commit GitHub does not have gives
    # 404 or 422, recorded as null: atlas-darkroom was pinned at a commit that
    # existed only in the owner's clone (verifier-P0, 2026-09-29).
    pins = {}
    for name, cfg in sorted(PINS["repos"].items()):
        out = gh("api", "repos/%s/commits/%s" % (full(name), cfg["commit"]), "--jq", ".sha", allow_missing=True)
        pins[name] = {"commit": cfg["commit"], "sha": out.strip() if out else None}

    # Every workflow of every pinned repository, so that pins.json must class
    # each one: verifier-P0 found two repositories' test workflows passing
    # while Home showed a dash, because nothing had declared them.
    workflows = {}
    for name in sorted(PINS["repos"]):
        workflows[name] = sorted(lines_json(gh("api", "--paginate", "repos/%s/actions/workflows" % full(name),
                                               "--jq", ".workflows[] | .name | @json")))

    runs = {}
    for name, cfg in sorted(PINS["repos"].items()):
        wanted = [w for w, c in cfg.get("workflows", {}).items() if c == "verifies"]
        if not wanted:
            continue
        got = lines_json(gh("api", "--paginate", "repos/%s/actions/runs?per_page=100" % full(name),
                            "--jq", ".workflow_runs[] | {workflow: .name, sha: .head_sha, branch: .head_branch, "
                                    "status: .status, conclusion: .conclusion, created: .created_at, url: .html_url}"))
        mine = [r for r in got if r["workflow"] in wanted]
        runs[name] = sorted(mine, key=lambda r: (r["created"], r["sha"]))

    now = datetime.datetime.now().astimezone()
    snap = {
        "taken": now.isoformat(timespec="seconds"),
        "owner": OWNER,
        "owners": owners,
        "command": "python site/snapshot_github.py (gh repo list and gh api; see its docstring)",
        "repos": sorted(repos, key=lambda r: r["name"].lower()),
        "github_only": github_only,
        "pins": pins,
        "workflows": workflows,
        "runs": runs,
    }
    # Named to the minute: a second snapshot on one day is a new file, never a
    # silent overwrite of the one a published build was read from.
    out = ROOT / "sources" / ("github-%s.json" % now.strftime("%Y-%m-%d-%H%M"))
    if out.exists():
        sys.exit("%s exists; a snapshot is never overwritten" % out.relative_to(ROOT))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print("wrote %s: %d repositories, %d read through the API only, CI runs for %s"
          % (out.relative_to(ROOT).as_posix(), len(repos), len(github_only),
             ", ".join("%s (%d)" % (k, len(v)) for k, v in runs.items())))
    missing = sorted(k for k, v in pins.items() if not v["sha"])
    if missing:
        print("NOT ON GITHUB: %s; the build refuses these pins"
              % ", ".join("%s@%s" % (k, pins[k]["commit"]) for k in missing))


if __name__ == "__main__":
    main()

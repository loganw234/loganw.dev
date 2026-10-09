"""Make a parcel's planted copy for its verifier (docs/ROUND2.md, "Planted faults").

    python make_plant.py <key.json>

key.json: {"parcel": "P1", "commit": "<the parcel's commit>", "branch": "r2-plant-P1",
           "plants": [{"file": "...", "old": "...", "new": "...", "kind": "...", "why": "..."}, ...]}

1. A detached worktree at the parcel's commit, under this script's folder.
2. Each plant applied as an exact replacement that must match once.
3. public/ rebuilt (python site/build.py, with LOGANW_REPOS and the site's .cache).
4. One commit with the parcel's own parent, message, author and committer,
   whose tree is the parcel's plus the plants: `git commit-tree`.
5. The branch named in the key, at that commit, in the lead's repository.
6. The worktree is left checked out at the planted commit, for the full gate;
   remove it after with `git worktree remove --force`.

Prints the planted commit and the key's SHA-256. The key stays out of the
ledger until the last planted-copy verifier has reported.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

# The lead ran it with these two paths written in; archived, it reads them from the
# environment: LOGANW_DEV is the lead's clone of loganw.dev, LOGANW_REPOS the directory
# that holds the owner's clones.
REPO = pathlib.Path(os.environ["LOGANW_DEV"])
REPOS = os.environ["LOGANW_REPOS"]
HERE = pathlib.Path(__file__).resolve().parent


def git(*args, cwd=REPO, env=None, inp=None):
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, env=env, input=inp)
    if r.returncode:
        sys.exit("git %s: %s" % (" ".join(args), r.stderr.decode("utf-8", "replace")))
    return r.stdout.decode("utf-8", "replace")


def main():
    key_path = pathlib.Path(sys.argv[1])
    key = json.loads(key_path.read_text(encoding="utf-8"))
    sha = git("rev-parse", key["commit"]).strip()
    wt = HERE / ("plant-" + key["parcel"])
    if wt.exists():
        sys.exit("%s exists; remove it first" % wt)
    git("worktree", "add", "--detach", str(wt), sha)
    for p in key["plants"]:
        f = wt / p["file"]
        t = f.read_text(encoding="utf-8")
        n = t.count(p["old"])
        if n != 1:
            sys.exit("%s: the plant's old text matches %d times" % (p["file"], n))
        f.write_bytes(t.replace(p["old"], p["new"]).encode("utf-8"))
    shutil.copytree(REPO / ".cache", wt / ".cache")
    env = dict(os.environ, LOGANW_REPOS=REPOS)
    r = subprocess.run([sys.executable, "site/build.py"], cwd=wt, env=env, capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-500:])
    if r.returncode:
        sys.exit("the build refused the planted tree")
    git("add", "-A", cwd=wt)
    tree = git("write-tree", cwd=wt).strip()
    parent = git("rev-parse", sha + "^").strip()
    fmt = git("show", "-s", "--format=%an%x00%ae%x00%aD%x00%cn%x00%ce%x00%cD", sha).split("\x00")
    msg = git("show", "-s", "--format=%B", sha)
    cenv = dict(os.environ, GIT_AUTHOR_NAME=fmt[0], GIT_AUTHOR_EMAIL=fmt[1], GIT_AUTHOR_DATE=fmt[2],
                GIT_COMMITTER_NAME=fmt[3], GIT_COMMITTER_EMAIL=fmt[4], GIT_COMMITTER_DATE=fmt[5].strip())
    planted = git("commit-tree", tree, "-p", parent, env=cenv, inp=msg.encode("utf-8")).strip()
    git("branch", "-f", key["branch"], planted)
    git("checkout", "--detach", planted, cwd=wt)
    print("parcel commit  ", sha)
    print("planted commit ", planted, "on", key["branch"])
    print("diff, for the lead only:")
    print(git("diff", "--stat", sha, planted))
    print("key SHA-256    ", hashlib.sha256(key_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

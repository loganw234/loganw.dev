#!/bin/bash
# The front door: does the site still hold? Adapted from HonestFramework's
# templates/gate-runner.sh (MIT); its reasoning is kept in the comments.
#
#   bash verify/run.sh                  every stage (~15 s on the desktop)
#   bash verify/run.sh --require-all    a skipped stage, or a figure skipped inside one, FAILS
#   bash verify/run.sh --list           the stages, with * on what this invocation would run
#   bash verify/run.sh --only a,b       by name; an unknown name is refused
#   bash verify/run.sh --skip a
#   bash verify/run.sh --resume         continue the last run of this commit
#
# The desktop has every pinned clone, private ones included, and is the one
# host that can run every stage: run it with --require-all before any push.
# CI has only the public repositories (it fetches them at their pins), so its
# `build` stage and its private figures are SKIPPED BY NAME, never passed.
#
# THERE IS NO CACHE ACROSS RUNS. --resume skips what already passed in this
# run id; a fresh invocation runs everything again.
set -uo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
STATEROOT="${STATEROOT:-$ROOT/verify/state}"
PY="${PYTHON:-python}"
command -v "$PY" >/dev/null 2>&1 || PY=python3

ONLY=""; SKIP=""; REQUIRE_ALL=0; LIST=0; RESUME=""; FRESH=0

die () { echo "FATAL: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --only)        [ $# -ge 2 ] || die "--only needs a list"; ONLY="$ONLY,$2"; shift 2;;
    --skip)        [ $# -ge 2 ] || die "--skip needs a list"; SKIP="$SKIP,$2"; shift 2;;
    --require-all) REQUIRE_ALL=1; shift;;
    --list)        LIST=1; shift;;
    --resume)      if [ $# -gt 1 ] && [[ ${2:-} != --* ]]; then RESUME=$2; shift 2
                   else RESUME=last; shift; fi;;
    --fresh)       FRESH=1; shift;;
    -h|--help)     sed -n '2,20p' "$0"; exit 0;;
    *)             die "unknown option $1";;
  esac
done

in_list() { case ",$2," in *",$1,"*) return 0;; esac; return 1; }

# The only copy of the stage list is the `stage` calls below.
SELF="${BASH_SOURCE[0]}"
STAGELIST=$(grep -E '^stage [a-z0-9-]+ "' "$SELF" | awk '{print $2}' | tr '\n' ' ')
STAGELIST="${STAGELIST% }"

if [ "$LIST" = 1 ]; then
  while IFS=$'\t' read -r _nm _ds; do
    if [ -z "$ONLY" ] || in_list "$_nm" "$ONLY"; then _mk="*"; else _mk=" "; fi
    printf '%s %-14s%s\n' "$_mk" "$_nm" "$_ds"
  done < <(grep -E '^stage [a-z0-9-]+ "' "$SELF" | sed -E 's/^stage ([a-z0-9-]+) +"([^"]*)".*/\1\t\2/')
  echo
  if [ -n "$ONLY" ]; then echo "* = would run. Unmarked stages are NOT in this selection."
  else echo "* = would run: every stage."; fi
  exit 0
fi

check_names() {
  local n
  for n in $(echo "$2" | tr ',' ' '); do
    [ -z "$n" ] && continue
    case " $STAGELIST " in
      *" $n "*) ;;
      *) echo "ERROR: $1 names unknown stage '$n'" >&2; echo "       stages: $STAGELIST" >&2; exit 2;;
    esac
  done
}
check_names --only "$ONLY"
check_names --skip "$SKIP"

COMMIT=$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo nogit)
[ -n "$(git -C "$ROOT" status --porcelain 2>/dev/null)" ] && COMMIT="$COMMIT-dirty"
if [ -n "$RESUME" ] && [ "$FRESH" = 1 ]; then die "--resume and --fresh are contradictory"; fi
if [ -n "$RESUME" ]; then
  if [ "$RESUME" = last ]; then
    RUNID=$(ls -1 "$STATEROOT" 2>/dev/null | sort | tail -n 1)
    [ -n "$RUNID" ] || die "--resume: no previous run under $STATEROOT"
  else RUNID=$RESUME; fi
  case "$RUNID" in
    *-"$COMMIT") ;;
    *) die "run $RUNID was a different tree than $COMMIT; half a run of one tree glued to half a run of another is a report about neither. Use --fresh.";;
  esac
else
  RUNID="$(date +%Y%m%d-%H%M%S)-$COMMIT"
fi
RUNDIR="$STATEROOT/$RUNID"
mkdir -p "$RUNDIR"
JSONL="$RUNDIR/stages.jsonl"
PASSED=0; FAILED=0; SKIPPED=0; CACHED=0; INNER=0
note () { echo "   $*"; }
echo "== run $RUNID"
echo "   commit $COMMIT, python $("$PY" --version 2>&1), state in $RUNDIR"

# stage <name> <description> -- command...
# MUST_FAIL=1 before a stage inverts it: the command must fail, and its
# success is the failure. Exit 3 from a command means "this machine cannot
# read a source it needs" and is a SKIP by name, with the command's reason.
stage() {
  local name=$1 desc=$2; shift 3
  local t0 t1 rc verdict="" reason="" expect_fail="${MUST_FAIL:-0}"
  MUST_FAIL=0
  if [ -n "$ONLY" ] && ! in_list "$name" "$ONLY"; then return 0; fi
  if [ -f "$RUNDIR/$name.ok" ]; then
    CACHED=$((CACHED+1)); note "$(printf '%-14s %-7s %s' "$name" "ok" "(passed earlier in this run)")"; return 0
  fi
  if in_list "$name" "$SKIP"; then verdict=SKIP; reason="requested"; fi
  if [ -z "$verdict" ]; then
    t0=$(date +%s)
    "$@" > "$RUNDIR/$name.log" 2>&1
    rc=$?
    t1=$(date +%s)
    if [ "$rc" -eq 3 ] && [ "$expect_fail" != 1 ]; then
      verdict=SKIP; reason=$(grep -m1 '^UNAVAILABLE' "$RUNDIR/$name.log" || echo "a source is unavailable here")
    fi
  fi
  if [ "$verdict" = SKIP ]; then
    SKIPPED=$((SKIPPED+1))
    note "$(printf '%-14s %-7s %s' "$name" "SKIP" "$reason")"
    echo "{\"stage\":\"$name\",\"verdict\":\"skip\"}" >> "$JSONL"
    [ "$REQUIRE_ALL" = 1 ] && FAILED=$((FAILED+1))
    return 0
  fi
  if [ "$expect_fail" = 1 ]; then
    # Only a check that ran and said no (rc 1) is the failure this wants. A
    # refusal or an unavailable source (rc 2, 3) means the control never ran.
    if [ "$rc" -ne 1 ]; then
      FAILED=$((FAILED+1))
      if [ "$rc" -eq 0 ]; then
        note "$(printf '%-14s %-7s %s' "$name" "FAIL" "NEGATIVE CONTROL DID NOT FAIL - this runner cannot see a failing check")"
      else
        note "$(printf '%-14s %-7s %s' "$name" "FAIL" "the control did not run (rc=$rc); see $RUNDIR/$name.log")"
      fi
      echo "{\"stage\":\"$name\",\"verdict\":\"control-broken\",\"rc\":$rc}" >> "$JSONL"
      return 1
    fi
    rc=0; note "$(printf '%-14s %-7s %s' "$name" "ok" "(failed, as it must: $(tail -n 1 "$RUNDIR/$name.log"))")"
  fi
  if [ "$rc" -eq 0 ]; then
    # A stage can pass while skipping things inside it: count those too, or the
    # verdict says "nothing skipped" over them (cft-fp256 met this in its round
    # 3, and this runner's first run without clones did the same: "1 skipped"
    # over 118 figures skipped inside a passing stage).
    local inner
    inner=$(grep -o -E '[0-9]+ skipped by name' "$RUNDIR/$name.log" | tail -n 1 | awk '{print $1}')
    [ -n "$inner" ] && [ "$inner" -gt 0 ] && INNER=$((INNER+inner))
    : > "$RUNDIR/$name.ok"; PASSED=$((PASSED+1))
    [ "$expect_fail" = 1 ] || note "$(printf '%-14s %-7s %3ss  %s' "$name" "ok" "$((t1-t0))" "$(tail -n 1 "$RUNDIR/$name.log")")"
    echo "{\"stage\":\"$name\",\"verdict\":\"ok\",\"seconds\":$((t1-t0))}" >> "$JSONL"
  else
    : > "$RUNDIR/$name.fail"; FAILED=$((FAILED+1))
    note "$(printf '%-14s %-7s rc=%s  see %s' "$name" "FAIL" "$rc" "$RUNDIR/$name.log")"
    echo "{\"stage\":\"$name\",\"verdict\":\"fail\",\"rc\":$rc}" >> "$JSONL"
  fi
}

B="$ROOT/site/build.py"
RA=""; [ "$REQUIRE_ALL" = 1 ] && RA="--require-all"

# ======================================================================
# THE STAGES. One `stage` line each; the description stays on the line.
# ======================================================================
stage build "public/ is exactly what the pins render; needs every pinned clone, private ones too" -- "$PY" "$B" --check
stage facts "every published figure read again at its pin; a private one is skipped by name" -- "$PY" "$B" --verify-facts $RA
stage links "every relative link and src in public/ resolves" -- "$PY" "$B" --links
stage local-only "nothing in public/ loads from another host, and no page runs a script" -- "$PY" "$B" --local-only
stage docs "the documents' relative links resolve and the counts they state are true" -- "$PY" "$B" --docs
stage controls "a planted fault for each check above, each caught by name" -- "$PY" "$B" --control
# The runner's own control: a real check pointed at a planted copy. If this
# stage passes, the runner cannot tell a failing check from a passing one.
MUST_FAIL=1
stage runner-control "the links check on a copy with a broken link MUST fail" -- "$PY" "$B" --planted-link
# ======================================================================

echo "== summary"
echo "   passed $PASSED, failed $FAILED, skipped $SKIPPED, cached $CACHED; record $JSONL"
if [ "$FAILED" -ne 0 ]; then echo "VERDICT: FAIL"; exit 1; fi
if [ "$SKIPPED" -ne 0 ] || [ "$INNER" -ne 0 ]; then
  echo "VERDICT: PASS, with $SKIPPED stage(s) and $INNER figure(s) inside passing stages skipped by name (--require-all makes a skip a failure)"
  exit 0
fi
echo "VERDICT: PASS, nothing skipped"
exit 0

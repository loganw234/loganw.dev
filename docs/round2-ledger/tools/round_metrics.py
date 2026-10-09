"""loganw.dev round 2's metrics, read from the session's transcripts. Read-only.

    python round_metrics.py <lead transcript .jsonl> <round start, ISO UTC> [<cutoff, ISO UTC>]

The lead's transcript is one JSONL file; each agent's is <session>/subagents/
agent-<id>.jsonl, with agent-<id>.meta.json beside it, where <session> is the
lead's transcript's path without ".jsonl".

What it counts, and how (ParcelRound's case studies 6 and 7 are the method):
- The round's agents are the ones whose description starts with "R2 ". A
  description "R2 P<n>..." is a parcel; "R2 verifier..." a verifier; any other
  "R2 " agent is counted as "other".
- Tokens are summed from each agent's own transcript, and the lead's from its
  own, once per message id, from that message's last usage record, between
  the round's start and the cutoff. Fresh tokens are input, cache writes and
  output; cache reads are counted apart, and so is output on its own.
- The model is read from the agent's own transcript (each assistant
  message's "model"), never from its brief.
- A run is one stretch of an agent's work: a task notification carrying a
  usage block. A later notification of the same task with the same implied
  start (its time less its duration, within 3 s) is the same run, and its
  figures replace the earlier one's (case study 7: some notifications repeat,
  with cumulative figures). Tool uses and minutes are the runs' own figures.
- The runtime's "subagent_tokens" is the agent's context size at the run's
  end (case study 7), so it is printed as "context at end", never as usage.
- An agent with no notification yet is still running: its row says so, and its
  tokens so far are counted.
- The lead's tool uses are its own tool_use blocks in the window; its time is
  the window's wall clock.
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

LOCAL = timezone(timedelta(hours=-7))
USAGE = re.compile(r"<subagent_tokens>(\d+)</subagent_tokens>\s*<tool_uses>(\d+)</tool_uses>\s*"
                   r"<duration_ms>(\d+)</duration_ms>")
TASK = re.compile(r"<task-id>([^<]+)</task-id>")


def when(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def texts(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from texts(v)


def usage_of(path, start, cut):
    """-> per-message usage summed, tool_use count, models, first and last timestamps."""
    last = {}
    tools = set()
    models = {}
    first = latest = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("type") != "assistant":
                continue
            m = r.get("message")
            t = r.get("timestamp")
            if not isinstance(m, dict) or not t:
                continue
            ts = when(t)
            if ts < start or (cut and ts > cut):
                continue
            first = first or ts
            latest = ts
            if m.get("usage"):
                last[m.get("id")] = m["usage"]
            if m.get("model"):
                models[m["model"]] = models.get(m["model"], 0) + 1
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools.add(c.get("id"))
    tot = {"messages": len(last), "input": 0, "cache_write": 0, "output": 0, "cache_read": 0}
    for u in last.values():
        tot["input"] += u.get("input_tokens", 0)
        tot["cache_write"] += u.get("cache_creation_input_tokens", 0)
        tot["output"] += u.get("output_tokens", 0)
        tot["cache_read"] += u.get("cache_read_input_tokens", 0)
    tot["fresh"] = tot["input"] + tot["cache_write"] + tot["output"]
    return tot, len(tools), models, first, latest


def notifications(lead, start, cut):
    """-> {task id: [[start, end, tool uses, ms, context], ...]}, one entry a run."""
    rows, seen = [], set()
    with open(lead, encoding="utf-8", errors="replace") as f:
        for line in f:
            if "subagent_tokens" not in line or "<task-notification>" not in line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            # A notification that arrives while the lead is working is kept as an
            # "attachment" record, not a "user" one; the same notification is
            # never counted twice (the `seen` key below).
            if r.get("type") not in ("user", "attachment") or not r.get("timestamp"):
                continue
            ts = when(r["timestamp"])
            if ts < start or (cut and ts > cut):
                continue
            # A "user" record holds the notification under "message"; an
            # "attachment" record under "attachment.prompt" and its renderings.
            # Every string in the record is read, and `seen` counts each once.
            for t in texts(r):
                for block in t.split("<task-notification>")[1:]:
                    u, k = USAGE.search(block), TASK.search(block)
                    if not (u and k):
                        continue
                    key = (k.group(1), u.group(1), u.group(3))
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append((k.group(1), ts, int(u.group(1)), int(u.group(2)), int(u.group(3))))
    runs = {}
    for task, ts, ctx, tools, ms in sorted(rows, key=lambda x: (x[0], x[1])):
        begun = ts - timedelta(milliseconds=ms)
        lst = runs.setdefault(task, [])
        if lst and abs((lst[-1][0] - begun).total_seconds()) <= 3:
            lst[-1][1:] = [ts, tools, ms, ctx]
        else:
            lst.append([begun, ts, tools, ms, ctx])
    return runs


def main():
    lead, start = sys.argv[1], when(sys.argv[2])
    cut = when(sys.argv[3]) if len(sys.argv) > 3 else None
    session = lead[:-len(".jsonl")]
    runs = notifications(lead, start, cut)
    agents = []
    for meta_path in sorted(glob.glob(os.path.join(session, "subagents", "agent-*.meta.json"))):
        meta = json.load(open(meta_path, encoding="utf-8"))
        desc = meta.get("description", "")
        if not desc.startswith("R2 "):
            continue
        aid = os.path.basename(meta_path)[len("agent-"):-len(".meta.json")]
        tot, tools, models, first, latest = usage_of(meta_path.replace(".meta.json", ".jsonl"), start, cut)
        if first is None:
            continue
        klass = "parcel" if re.match(r"R2 P\d", desc) else "verifier" if desc.startswith("R2 verifier") else "other"
        rr = runs.get(aid, [])
        agents.append({"desc": desc[3:], "class": klass, "requested": meta.get("model", ""),
                       "model": ", ".join(sorted(models)), "runs": len(rr),
                       "minutes": sum(x[3] for x in rr) / 60000 if rr else None,
                       "tools": sum(x[2] for x in rr) if rr else tools,
                       "context_end": rr[-1][4] if rr else None, "first": first, **tot})
    agents.sort(key=lambda a: a["first"])
    ltot, ltools, lmodels, lfirst, llatest = usage_of(lead, start, cut)
    end = cut or llatest

    def m(x):
        return "%.1f M" % (x / 1e6) if x >= 1e6 else "%.0f k" % (x / 1e3)

    print("Window: %s to %s (local, UTC-7): %.0f minutes of wall clock."
          % (start.astimezone(LOCAL).strftime("%Y-%m-%d %H:%M:%S"), end.astimezone(LOCAL).strftime("%Y-%m-%d %H:%M:%S"),
             (end - start).total_seconds() / 60))
    print()
    print("| agent | class | model (from its transcript) | runs | minutes | tool uses | messages | output | fresh | cache reads | context at end |")
    print("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for a in agents:
        mins = "%.0f" % a["minutes"] if a["minutes"] is not None else "running"
        ctx = "{:,}".format(a["context_end"]) if a["context_end"] is not None else "-"
        print("| %s | %s | %s | %d | %s | %d | %d | %s | %s | %s | %s |"
              % (a["desc"], a["class"], a["model"], a["runs"], mins, a["tools"], a["messages"], m(a["output"]),
                 m(a["fresh"]), m(a["cache_read"]), ctx))
    print("| the lead | lead | %s | - | %.0f (wall) | %d | %d | %s | %s | %s | - |"
          % (", ".join(sorted(lmodels)), (end - start).total_seconds() / 60, ltools, ltot["messages"],
             m(ltot["output"]), m(ltot["fresh"]), m(ltot["cache_read"])))
    print()
    classes = {}
    for a in agents:
        c = classes.setdefault(a["class"], {"agents": 0, "runs": 0, "minutes": 0.0, "tools": 0, "output": 0,
                                            "fresh": 0, "cache_read": 0})
        c["agents"] += 1
        c["runs"] += a["runs"]
        c["minutes"] += a["minutes"] or 0
        c["tools"] += a["tools"]
        for k in ("output", "fresh", "cache_read"):
            c[k] += a[k]
    print("| class | agents | runs | agent-minutes | tool uses | output | fresh | cache reads |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    allc = {"agents": 0, "runs": 0, "minutes": 0.0, "tools": 0, "output": 0, "fresh": 0, "cache_read": 0}
    for k in ("parcel", "verifier", "other"):
        if k in classes:
            c = classes[k]
            print("| %ss | %d | %d | %.0f | %d | %s | %s | %s |" % (k, c["agents"], c["runs"], c["minutes"], c["tools"],
                                                                   m(c["output"]), m(c["fresh"]), m(c["cache_read"])))
            for x in allc:
                allc[x] += c[x]
    print("| the lead | 1 | - | - | %d | %s | %s | %s |" % (ltools, m(ltot["output"]), m(ltot["fresh"]),
                                                          m(ltot["cache_read"])))
    print("| **all** | **%d** | **%d** | **%.0f** | **%d** | **%s** | **%s** | **%s** |"
          % (allc["agents"] + 1, allc["runs"], allc["minutes"], allc["tools"] + ltools, m(allc["output"] + ltot["output"]),
             m(allc["fresh"] + ltot["fresh"]), m(allc["cache_read"] + ltot["cache_read"])))
    if allc["output"] + ltot["output"]:
        v = classes.get("verifier", {}).get("output", 0)
        print()
        print("Verifiers' share of output: %.1f%%; parcels' %.1f%%; the lead's %.1f%%."
              % tuple(100.0 * x / (allc["output"] + ltot["output"])
                      for x in (v, classes.get("parcel", {}).get("output", 0), ltot["output"])))


if __name__ == "__main__":
    main()

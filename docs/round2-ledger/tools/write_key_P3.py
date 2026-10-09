"""Write P3's key (a script file, not a heredoc: CLAUDE.md trap 8)."""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
import os
# Archived: the lead's clone of loganw.dev is read from LOGANW_DEV.
src = subprocess.run(["git", "-C", os.environ["LOGANW_DEV"], "show",
                      "583d3eb:site/pages/thread_film.py"], capture_output=True).stdout.decode("utf-8")
BS = chr(92)  # a backslash, built from its code point

old1 = ('          r"31' + BS + '.1%, and coherences of ' + BS + '+0' + BS + '.27 to ' + BS + '+0' + BS +
        '.34 where a classical mixture gives 0' + BS + '. And all three fall "\n'
        '          r"short of what their own noise models predicted' + BS + '.)$"),')
new1 = ('          r"31' + BS + '.1%, and coherences of ' + BS + '+0' + BS + '.27 to ' + BS + '+0' + BS +
        '.34 where a classical mixture gives 0' + BS + '.) And all three fall "\n'
        '          r"short of what their own noise models predicted' + BS + '.$"),')
old2 = ('"\u201d. Below, one of the devices\' prints, with the device, the job and the rule that laid it read from the "')
new2 = ('"\u201d. Below, the print of the device whose run came closest to its noise model\'s prediction, with the '
        'device, the job and the rule that laid it read from the "')
for o in (old1, old2):
    print(src.count(o), repr(o[:80]))
key = {"parcel": "P3", "commit": "583d3eb", "branch": "r2-plant-P3", "verifier": "verifier-P3", "plants": [
    {"file": "site/pages/thread_film.py", "old": old1, "new": new1,
     "kind": "a quote cut short, so the page claims more than its source",
     "why": "docs/HARDWARE-RESULTS.md line 5's one-paragraph summary gives the agreement and, in its next sentence, "
            "that all three devices fall short of their noise models' predictions. The plant ends the quote before "
            "that sentence, so the page reports the agreement without the shortfall; P3's brief names this trap."},
    {"file": "site/pages/thread_film.py", "old": old2, "new": new2,
     "kind": "a sentence that claims more than its source (a selection reason no source gives)",
     "why": "The device was chosen as first in the pre-registered order, which the next paragraph quotes; no "
            "source on the page says ibm_kingston's run came closest to its noise model's prediction, and the "
            "results document says all three fall short."}]}
(HERE / "keys" / "key-P3.json").write_text(json.dumps(key, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                           newline="\n")
print("key written")

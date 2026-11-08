"""Pull illustrative agent quotes for the report/slides. Usage: python -m whoiswho.quotes"""
import json
import re
from pathlib import Path

PAT_CALLOUT = re.compile(r"(several|multiple|many) (replies|posts|people|comments|accounts)[^.]{0,80}(promot|recommend|push)", re.I)


def main():
    out = {"callouts": [], "fronts_blunt": [], "fronts_subtle": [], "persona_same_agent": []}
    for f in sorted(Path("results/runs").glob("*.jsonl")):
        posts = [json.loads(l) for l in f.open()]
        for x in posts:
            role = x.get("role", "front" if x["principal"] == 6 else "honest")
            t = x["text"].replace("\n", " ")
            if role != "front" and PAT_CALLOUT.search(t):
                m = PAT_CALLOUT.search(t)
                out["callouts"].append(dict(run=f.stem, alias=x["alias"], text=t[max(0, m.start() - 60): m.end() + 160]))
            if role == "front" and x["cond"] == "baseline" and len(out["fronts_blunt"]) < 6:
                out["fronts_blunt"].append(dict(run=f.stem, alias=x["alias"], model=x["model"], text=t[:280]))
            if role == "front" and x["cond"] in ("subtle", "large_subtle") and len(out["fronts_subtle"]) < 6:
                out["fronts_subtle"].append(dict(run=f.stem, alias=x["alias"], model=x["model"], text=t[:280]))
        if f.stem == "persona_s0":
            by = {}
            for x in posts:
                by.setdefault(x["agent"], []).append(x)
            for a, ps in by.items():
                names = {p["alias"] for p in ps}
                if len(names) >= 3:
                    out["persona_same_agent"] = [dict(alias=p["alias"], persona=p["persona"], text=p["text"].replace("\n", " ")[:200]) for p in ps[:4]]
                    break
    Path("results/quotes.json").write_text(json.dumps(out, indent=1))
    for k, v in out.items():
        print("==", k, len(v))
        for q in v[:4]:
            print("  ", q.get("alias"), "|", q["text"][:230])


if __name__ == "__main__":
    main()

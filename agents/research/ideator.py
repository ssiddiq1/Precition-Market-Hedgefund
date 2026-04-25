import os
import time
from datetime import datetime, timezone

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTEXT_DIR = os.path.join(BASE_DIR, "context")
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
INTERVAL    = 24 * 3600  # once per day


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""


def parse_incomplete_items(master_text):
    """Return all unchecked '- [ ]' lines from master.md."""
    return [
        line.strip()[6:]
        for line in master_text.splitlines()
        if line.strip().startswith("- [ ]")
    ]


def last_analysis_blocks(analysis_text, n=2):
    """Return the last n blocks split by '---'."""
    if not analysis_text.strip():
        return []
    blocks = [b.strip() for b in analysis_text.strip().split("---") if b.strip()]
    return blocks[-n:]


def build_proposals(master_text, analysis_text):
    proposals = []

    incomplete = parse_incomplete_items(master_text)
    if incomplete:
        preview = "\n".join(f"  · {i}" for i in incomplete[:10])
        if len(incomplete) > 10:
            preview += f"\n  … and {len(incomplete) - 10} more"
        proposals.append({
            "type":  "PREP PLAN",
            "title": f"{len(incomplete)} incomplete checklist item(s) in master.md",
            "body":  preview,
        })

    blocks = last_analysis_blocks(analysis_text)
    for i, block in enumerate(blocks, 1):
        # Surface specific signals worth investigating
        lines = [l for l in block.splitlines() if l.startswith("-")]
        if not lines:
            continue
        proposals.append({
            "type":  "RESEARCH",
            "title": f"Follow-up on analysis block {i}",
            "body":  "\n".join(f"  {l}" for l in lines[:8]),
        })

    if not proposals:
        proposals.append({
            "type":  "RESEARCH",
            "title": "No actionable data yet",
            "body":  "  Paste master doc and run analyst.py to generate insights.",
        })

    return proposals


def run_ideation():
    os.makedirs(LOGS_DIR, exist_ok=True)
    master_text   = read_file(os.path.join(CONTEXT_DIR, "master.md"))
    analysis_text = read_file(os.path.join(LOGS_DIR, "analysis.md"))
    ts            = datetime.now(timezone.utc).isoformat()

    proposals = build_proposals(master_text, analysis_text)
    approved  = []

    print(f"\n[ideator] {len(proposals)} proposal(s) — {ts}\n")
    for p in proposals:
        print(f"  [{p['type']}] {p['title']}")
        print(p["body"])
        try:
            answer = input("  Update master doc? (y/n): ").strip().lower()
        except EOFError:
            answer = "n"
        if answer == "y":
            approved.append(p)
        print()

    log_path = os.path.join(LOGS_DIR, "proposed_updates.md")
    with open(log_path, "a") as f:
        f.write(f"\n## Proposals — {ts}\n\n")
        for p in proposals:
            status = "APPROVED" if p in approved else "SKIPPED"
            f.write(f"### [{status}] [{p['type']}] {p['title']}\n{p['body']}\n\n")

    print(f"[ideator] {len(approved)}/{len(proposals)} approved → {log_path}")


def main():
    print(f"[ideator] Running daily → {LOGS_DIR}/proposed_updates.md")
    while True:
        try:
            run_ideation()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"[ideator ERROR] {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    import sys
    if "--once" in sys.argv:
        run_ideation()
    else:
        main()

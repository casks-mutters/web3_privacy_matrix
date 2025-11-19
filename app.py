#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional


@dataclass
class PrivacyStack:
    key: str
    name: str
    family: str
    description: str
    privacy_level: int        # 1–10
    soundness_focus: int      # 1–10
    performance_cost: int     # 1–10 (higher = more expensive)
    dev_complexity: int       # 1–10
    ecosystem_maturity: int   # 1–10


STACKS: Dict[str, PrivacyStack] = {
    "aztec": PrivacyStack(
        key="aztec",
        name="Aztec-style zk Rollup",
        family="zk-SNARK privacy L2",
        description="Encrypted L2 state and zero-knowledge proofs over Ethereum.",
        privacy_level=9,
        soundness_focus=8,
        performance_cost=7,
        dev_complexity=8,
        ecosystem_maturity=7,
    ),
    "zama": PrivacyStack(
        key="zama",
        name="Zama-style FHE Compute",
        family="FHE + Web3",
        description="Fully homomorphic encryption over on-chain or off-chain data.",
        privacy_level=8,
        soundness_focus=9,
        performance_cost=9,
        dev_complexity=9,
        ecosystem_maturity=5,
    ),
    "soundness": PrivacyStack(
        key="soundness",
        name="Soundness-first Lab",
        family="Formal verification",
        description="Specification-driven, proof-oriented engineering for Web3 protocols.",
        privacy_level=6,
        soundness_focus=10,
        performance_cost=6,
        dev_complexity=7,
        ecosystem_maturity=8,
    ),
}


FIELDS_ORDER = [
    "key",
    "name",
    "family",
    "privacy_level",
    "soundness_focus",
    "performance_cost",
    "dev_complexity",
    "ecosystem_maturity",
]


def list_keys() -> List[str]:
    return list(STACKS.keys())


def to_dict(stack: PrivacyStack) -> Dict[str, Any]:
    return asdict(stack)


def score_stack(stack: PrivacyStack) -> float:
    # Composite score: privacy and soundness are benefits, cost and complexity are penalties.
    benefit = 0.45 * stack.privacy_level + 0.40 * stack.soundness_focus
    penalty = 0.10 * stack.performance_cost + 0.05 * stack.dev_complexity
    return round(benefit - penalty, 2)


def build_rows(selected: List[PrivacyStack], include_score: bool) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for s in selected:
        row = to_dict(s)
        if include_score:
            row["composite_score"] = score_stack(s)
        rows.append(row)
    return rows


def format_table(rows: List[Dict[str, Any]], include_score: bool) -> str:
    headers = FIELDS_ORDER.copy()
    if include_score:
        headers.append("composite_score")

    # Compute column widths
    col_widths: Dict[str, int] = {}
    for h in headers:
        col_widths[h] = len(h)
    for row in rows:
        for h in headers:
            value = row.get(h, "")
            col_widths[h] = max(col_widths[h], len(str(value)))

    # Build header line
    header_line = "  ".join(h.upper().ljust(col_widths[h]) for h in headers)
    separator = "  ".join("-" * col_widths[h] for h in headers)

    lines = [header_line, separator]
    for row in rows:
        line_parts = []
        for h in headers:
            value = str(row.get(h, ""))
            line_parts.append(value.ljust(col_widths[h]))
        lines.append("  ".join(line_parts))
    return "\n".join(lines)


def format_csv(rows: List[Dict[str, Any]], include_score: bool) -> str:
    headers = FIELDS_ORDER.copy()
    if include_score:
        headers.append("composite_score")

    def esc(v: Any) -> str:
        s = str(v)
        if any(c in s for c in [",", '"', "\n"]):
            s = '"' + s.replace('"', '""') + '"'
        return s

    out_lines = [",".join(headers)]
    for row in rows:
        out_lines.append(",".join(esc(row.get(h, "")) for h in headers))
    return "\n".join(out_lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="web3_privacy_matrix",
        description=(
            "Compare Web3 privacy and soundness stacks inspired by Aztec, Zama, "
            "and soundness-focused labs."
        ),
    )
    parser.add_argument(
        "--stack",
        choices=list_keys() + ["all"],
        default="all",
        help="Which stack to show (default: all).",
    )
    parser.add_argument(
        "--format",
        choices=["table", "csv", "json"],
        default="table",
        help="Output format (table, csv, json).",
    )
    parser.add_argument(
        "--include-score",
        action="store_true",
        help="Include composite_score field in the output.",
    )
    parser.add_argument(
        "--sort-by",
        choices=FIELDS_ORDER + ["composite_score"],
        default=None,
        help="Optional sort key for rows.",
    )
    parser.add_argument(
        "--descending",
        action="store_true",
        help="Sort in descending order.",
    )
    return parser.parse_args()


def select_stacks(key: str) -> List[PrivacyStack]:
    if key == "all":
        return list(STACKS.values())
    return [STACKS[key]]


def sort_rows(rows: List[Dict[str, Any]], sort_by: Optional[str], descending: bool) -> List[Dict[str, Any]]:
    if not sort_by:
        return rows
    return sorted(rows, key=lambda r: r.get(sort_by, 0), reverse=descending)


def main() -> None:
    args = parse_args()
    stacks = select_stacks(args.stack)
    rows = build_rows(stacks, include_score=args.include_score)

    # If sorting by composite_score and it's not included yet, compute it temporarily.
    if args.sort_by == "composite_score" and not args.include_score:
        for r in rows:
            key = r["key"]
            r["composite_score"] = score_stack(STACKS[key])

    rows = sort_rows(rows, sort_by=args.sort_by, descending=args.descending)

    if args.format == "json":
        print(json.dumps(rows, indent=2, sort_keys=True))
    elif args.format == "csv":
        print(format_csv(rows, include_score=args.include_score or args.sort_by == "composite_score"))
    else:
        print(format_table(rows, include_score=args.include_score or args.sort_by == "composite_score"))


if __name__ == "__main__":
    main()

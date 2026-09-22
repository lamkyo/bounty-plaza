import argparse
import json
import sys
from .models import BountyInput
from .screen import assess_bounty


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Screen a bounty without claiming it")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--reward-usd", type=float)
    parser.add_argument("--source-url")
    args = parser.parse_args(argv)
    result = assess_bounty(BountyInput(args.title, args.description, args.reward_usd, args.source_url))
    print(json.dumps({"decision": result.decision.value, "claim_allowed": result.claim_allowed,
                      "reasons": result.reasons}, ensure_ascii=False))
    return 0 if result.claim_allowed else 2


if __name__ == "__main__":
    sys.exit(main())

"""Pure, deterministic bounty screening rules.

This module never claims an issue, sends money, or contacts an external service.
"""

import re
from .models import BountyAssessment, BountyInput, Decision

_NEGATIVE_MARKERS = (
    "negative bounty", "pay me", "pay the bounty", "reverse bounty",
    "stop spamming", "silly bounty",
)
_FINANCIAL_MARKERS = ("solana", "bitcoin", "ethereum", "monero", "crypto")
_CLAIM_MARKER = re.compile(r"(^|\W)/claim(?:\W|$)", re.IGNORECASE)


def _text(item: BountyInput) -> str:
    return f"{item.title}\n{item.description}".casefold()


def assess_bounty(item: BountyInput) -> BountyAssessment:
    """Assess an offer using conservative, explainable rules.

    Negative obligations are rejected even when the listing advertises a
    positive reward. Ambiguous financial language is held for human review.
    """
    text = _text(item)
    reasons: list[str] = []
    if any(marker in text for marker in _NEGATIVE_MARKERS):
        reasons.append("listing contains a negative or reverse-bounty obligation")
    if item.reward_usd is not None and item.reward_usd < 0:
        reasons.append("advertised reward is negative")
    if any(marker in text for marker in _FINANCIAL_MARKERS):
        reasons.append("cryptocurrency payment language requires human verification")
    if _CLAIM_MARKER.search(text):
        reasons.append("claim instruction is present; external action remains disabled")

    if any("negative" in reason or "reverse" in reason for reason in reasons):
        decision = Decision.REJECT
    elif reasons:
        decision = Decision.NEEDS_REVIEW
    else:
        decision = Decision.ELIGIBLE
    return BountyAssessment(decision, tuple(reasons), item.reward_usd)

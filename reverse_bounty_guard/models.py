from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    ELIGIBLE = "eligible"
    NEEDS_REVIEW = "needs_review"
    REJECT = "reject"


@dataclass(frozen=True)
class BountyInput:
    title: str
    description: str
    reward_usd: float | None = None
    source_url: str | None = None


@dataclass(frozen=True)
class BountyAssessment:
    decision: Decision
    reasons: tuple[str, ...]
    normalized_reward_usd: float | None

    @property
    def claim_allowed(self) -> bool:
        return self.decision == Decision.ELIGIBLE

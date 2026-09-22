from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    CLOSE = "close"
    ACCEPT = "accept"
    REVIEW = "review"


@dataclass(frozen=True)
class PullRequest:
    number: int
    author: str
    author_is_org_member: bool
    title: str = ""
    body: str = ""
    diff: str = ""


@dataclass(frozen=True)
class ReviewDecision:
    action: Action
    reason: str
    notification: str | None = None


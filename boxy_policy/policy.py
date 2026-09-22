from collections.abc import Iterable

from .models import Action, PullRequest, ReviewDecision


class BoxyPolicy:
    """Pure decision engine; GitHub I/O belongs in the caller/adapter."""

    def __init__(self, whitelist: Iterable[str] = (), team: str = "@OmniBlocks/coders"):
        self._whitelist = frozenset(self._normalise(name) for name in whitelist)
        self.team = team

    @staticmethod
    def _normalise(login: str) -> str:
        return login.strip().lstrip("@").casefold()

    def is_authorised(self, pr: PullRequest) -> bool:
        return pr.author_is_org_member or self._normalise(pr.author) in self._whitelist

    def evaluate(self, pr: PullRequest) -> ReviewDecision:
        if not self.is_authorised(pr):
            return ReviewDecision(
                Action.CLOSE,
                "author is not an organization member and is not whitelisted",
                f"{self.team}: please reopen PR #{pr.number} for review",
            )
        if self._removes_humor(pr.diff):
            return ReviewDecision(Action.CLOSE, "change appears to remove humor")
        if self._adds_humor(pr.diff):
            return ReviewDecision(Action.ACCEPT, "change appears to add humor")
        return ReviewDecision(Action.REVIEW, "authorized author; no humor policy match")

    @staticmethod
    def _removes_humor(diff: str) -> bool:
        removed = [line[1:].casefold() for line in diff.splitlines()
                   if line.startswith("-") and not line.startswith("---")]
        return any("humor" in line or "joke" in line or "funny" in line for line in removed)

    @staticmethod
    def _adds_humor(diff: str) -> bool:
        added = [line[1:].casefold() for line in diff.splitlines()
                 if line.startswith("+") and not line.startswith("+++")]
        return any("humor" in line or "joke" in line or "funny" in line for line in added)


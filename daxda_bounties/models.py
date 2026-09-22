from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass(frozen=True)
class Bounty:
    id: str
    title: str
    domain: str
    value_usd: int
    overview: str
    objectives: tuple[str, ...]
    technical_specification: tuple[str, ...]
    validation_criteria: tuple[str, ...]
    submission_format: tuple[str, ...]
    sub_bounty_opportunities: tuple[str, ...]
    parent_id: str | None = None
    def to_dict(self) -> dict[str, Any]: return asdict(self)
    def create_sub_bounty(self, *, suffix: str, title: str, domain: str, value_usd: int) -> "Bounty":
        if not suffix or not suffix.replace("-", "").isalnum(): raise ValueError("suffix must be URL-safe")
        if value_usd <= 0: raise ValueError("value_usd must be positive")
        return Bounty(f"{self.id}.{suffix}", title, domain, value_usd, self.overview, self.objectives, self.technical_specification, self.validation_criteria, self.submission_format, self.sub_bounty_opportunities, self.id)

@dataclass(frozen=True)
class ValidationReport:
    bounty_id: str
    checks: dict[str, bool] = field(default_factory=dict)
    @property
    def passed(self) -> int: return sum(self.checks.values())
    @property
    def total(self) -> int: return len(self.checks)
    @property
    def is_valid(self) -> bool: return self.total == 9 and self.passed == self.total

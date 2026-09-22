from .models import Bounty, ValidationReport

def validate_bounty(bounty: Bounty) -> ValidationReport:
    checks = {"has_identity": bool(bounty.id and bounty.title and bounty.domain), "positive_value": bounty.value_usd > 0, "overview_present": bool(bounty.overview.strip()), "objectives_present": bool(bounty.objectives), "technical_specification_present": bool(bounty.technical_specification), "validation_criteria_present": len(bounty.validation_criteria) >= 9, "submission_format_present": bool(bounty.submission_format), "recursive_opportunities_present": bool(bounty.sub_bounty_opportunities), "self_similar_contract": all(getattr(bounty, n) for n in ("overview", "objectives", "technical_specification", "submission_format"))}
    return ValidationReport(bounty.id, checks)
def validate_catalog(bounties: tuple[Bounty, ...]) -> dict[str, ValidationReport]: return {b.id: validate_bounty(b) for b in bounties}

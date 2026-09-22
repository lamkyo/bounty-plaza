from .models import Bounty

DAXDA_OVERVIEW = ("DAXDA is a recursive, self-similar bounty system for investigating difficult technical domains through independently verifiable specifications, artifacts, and validation gates. Each domain bounty can expand into smaller bounties while preserving the same contract and evidence standard.")
_DOMAINS = (("cl164", "Cl(16,4) Algebraic Structure", 7500), ("containment", "Containment and Stability", 7500), ("da13", "DA13 Differential Architecture", 7500), ("chrono", "Chrono-Temporal Reasoning", 7500), ("mmpibench", "MMPIBench Evaluation", 7000))

def _make(code: str, title: str, value: int) -> Bounty:
    return Bounty(f"DAXDA-{code.upper()}", f"DAXDA: {title}", code, value, DAXDA_OVERVIEW, ("Define a reproducible domain problem", "Produce an inspectable reference implementation", "Document limitations and follow-on work"), ("Python 3.10+ with deterministic inputs", "Versioned schemas and machine-readable artifacts", "No undisclosed network or credential dependencies"), ("schema-valid", "overview-identical", "domain-specific", "technical-complete", "tests-pass", "deterministic", "evidence-attached", "recursive", "submission-complete"), ("README.md", "src/ or package code", "tests/", "machine-readable manifest", "reproduction command"), ("benchmarking", "formal verification", "independent replication"))

META_BOUNTY = Bounty("BOUNTY-PLAZA-645", "DAXDA Recursive Bounty System", "meta", 37000, DAXDA_OVERVIEW, ("Publish five self-similar domain bounties",), ("Five domain contracts with a shared schema",), tuple(f"check-{i}" for i in range(1, 10)), ("catalog.json", "README.md", "tests/"), ("all domain bounties",))
BOUNTIES = tuple(_make(*item) for item in _DOMAINS)
def build_catalog() -> tuple[Bounty, ...]: return BOUNTIES

import json
from .catalog import BOUNTIES
from .validation import validate_catalog
def main() -> None:
    reports = validate_catalog(BOUNTIES)
    print(json.dumps({"bounties": [b.to_dict() for b in BOUNTIES], "validation": {k: {"passed": v.passed, "total": v.total, "valid": v.is_valid} for k, v in reports.items()}}, indent=2))
if __name__ == "__main__": main()

import json
import pytest
from daxda_bounties import BOUNTIES, META_BOUNTY, build_catalog, validate_bounty, validate_catalog

def test_catalog_has_five_domains_and_total():
    assert len(build_catalog()) == 5 and len({b.domain for b in BOUNTIES}) == 5
    assert sum(b.value_usd for b in BOUNTIES) == 37000
def test_every_bounty_passes_nine_checks():
    assert all(r.is_valid and r.passed == 9 and r.total == 9 for r in validate_catalog(BOUNTIES).values())
def test_contract_is_self_similar():
    assert all(b.overview == META_BOUNTY.overview and len(b.validation_criteria) >= 9 for b in BOUNTIES)
def test_sub_bounty_inherits_contract_and_parent():
    child = BOUNTIES[0].create_sub_bounty(suffix="replication-1", title="Replica", domain="replication", value_usd=100)
    assert child.parent_id == BOUNTIES[0].id and child.overview == BOUNTIES[0].overview and validate_bounty(child).is_valid
@pytest.mark.parametrize("suffix,value", [("", 1), ("bad suffix", 1), ("x", 0), ("x", -1)])
def test_sub_bounty_rejects_invalid_input(suffix, value):
    with pytest.raises(ValueError): BOUNTIES[0].create_sub_bounty(suffix=suffix, title="x", domain="x", value_usd=value)
def test_serialization_is_json_safe():
    assert "DAXDA-CL164" in json.dumps([b.to_dict() for b in BOUNTIES])

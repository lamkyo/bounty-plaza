import pytest

from saas_mode import Plan, SaaSMode, UsageExceeded, UnknownTenant


def test_create_and_authenticate_tenant_without_storing_plaintext_key():
    mode = SaaSMode()
    tenant, key = mode.create_tenant("acme", "pro")
    assert tenant.plan.name == "pro"
    assert mode.authenticate("acme", key) is tenant
    assert key not in repr(tenant)


def test_usage_is_metered_and_remaining_units_returned():
    mode = SaaSMode(plans=(Plan("tiny", 3),))
    mode.create_tenant("a", "tiny")
    assert mode.consume("a", 2) == 1
    assert mode.get_tenant("a").usage == 2


def test_quota_is_atomic_and_rejects_overage():
    mode = SaaSMode(plans=(Plan("tiny", 3),))
    mode.create_tenant("a", "tiny")
    with pytest.raises(UsageExceeded):
        mode.consume("a", 4)
    assert mode.get_tenant("a").usage == 0


@pytest.mark.parametrize("value", [0, -1])
def test_units_must_be_positive(value):
    mode = SaaSMode()
    mode.create_tenant("a")
    with pytest.raises(ValueError):
        mode.consume("a", value)


def test_invalid_credentials_and_unknown_tenant_fail_closed():
    mode = SaaSMode()
    mode.create_tenant("a")
    with pytest.raises(PermissionError):
        mode.authenticate("a", "wrong")
    # Accessing a non‑existent tenant should raise UnknownTenant
    with pytest.raises(UnknownTenant):
        mode.get_tenant("nonexistent")

"""In-memory SaaS mode.

The storage interface is deliberately small so an application can replace the
in-memory implementation with a database without changing its policy logic.
"""

from dataclasses import dataclass, field
from hashlib import sha256
import secrets


class SaaSError(Exception):
    """Base exception for SaaS-mode errors."""


class UnknownTenant(SaaSError):
    """Raised when a tenant identifier is not registered."""


class UsageExceeded(SaaSError):
    """Raised before an operation would exceed the tenant's quota."""


@dataclass(frozen=True)
class Plan:
    name: str
    monthly_units: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("plan name must not be empty")
        if self.monthly_units < 0:
            raise ValueError("monthly_units must be non-negative")


FREE = Plan("free", 100)
PRO = Plan("pro", 10_000)


@dataclass
class Tenant:
    tenant_id: str
    plan: Plan
    usage: int = 0
    _api_key_digest: str = field(repr=False, default="")

    @property
    def remaining_units(self) -> int:
        return self.plan.monthly_units - self.usage


class SaaSMode:
    """Tenant registry with fail-closed quota accounting.

    API keys are returned only at creation time; only their SHA-256 digest is
    retained. This class is intentionally not a billing or authentication
    provider.
    """

    def __init__(self, *, plans: tuple[Plan, ...] = (FREE, PRO)) -> None:
        self._plans = {plan.name: plan for plan in plans}
        self._tenants: dict[str, Tenant] = {}

    def create_tenant(self, tenant_id: str, plan: str = "free") -> tuple[Tenant, str]:
        tenant_id = tenant_id.strip()
        if not tenant_id:
            raise ValueError("tenant_id must not be empty")
        if tenant_id in self._tenants:
            raise ValueError("tenant already exists")
        try:
            selected = self._plans[plan]
        except KeyError as exc:
            raise ValueError(f"unknown plan: {plan}") from exc
        api_key = "sk_" + secrets.token_urlsafe(24)
        tenant = Tenant(tenant_id, selected, _api_key_digest=self._digest(api_key))
        self._tenants[tenant_id] = tenant
        return tenant, api_key

    def authenticate(self, tenant_id: str, api_key: str) -> Tenant:
        tenant = self._get(tenant_id)
        if not api_key or not secrets.compare_digest(tenant._api_key_digest, self._digest(api_key)):
            raise PermissionError("invalid credentials")
        return tenant

    def consume(self, tenant_id: str, units: int, *, api_key: str | None = None) -> int:
        tenant = self._get(tenant_id)
        if api_key is not None:
            self.authenticate(tenant_id, api_key)
        if units <= 0:
            raise ValueError("units must be positive")
        if tenant.usage + units > tenant.plan.monthly_units:
            raise UsageExceeded(f"quota exceeded for tenant {tenant_id}")
        tenant.usage += units
        return tenant.remaining_units

    def get_tenant(self, tenant_id: str) -> Tenant:
        return self._get(tenant_id)

    def _get(self, tenant_id: str) -> Tenant:
        try:
            return self._tenants[tenant_id]
        except KeyError as exc:
            raise UnknownTenant(tenant_id) from exc

    @staticmethod
    def _digest(api_key: str) -> str:
        return sha256(api_key.encode("utf-8")).hexdigest()


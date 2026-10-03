# src/service.py
from __future__ import annotations

from typing import Dict, Any, List

# Import the custom exception used by the tests.
# The exception is defined in ``exceptions.py``.
from .exceptions import UnknownTenant

class SaaSMode:
    def __init__(self, tenants: Dict[str, Dict[str, Any]]):
        self._tenants = tenants

    # ---------------------------------------------------------------------
    # Tenant lookup
    # ---------------------------------------------------------------------
    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Return tenant data for *tenant_id*.

        Raises
        """
        try:
            # Return a shallow copy to prevent accidental mutation of internal state
            return dict(self._tenants[tenant_id])
        except KeyError as exc:
            raise UnknownTenant(f"Tenant '{tenant_id}' not found") from exc

    # ---------------------------------------------------------------------
    # Utility
    # ---------------------------------------------------------------------
    def list_tenants(self) -> List[str]:
        """Return a list of all tenant identifiers currently stored.
        """
        return list(self._tenants.keys())

# End of module
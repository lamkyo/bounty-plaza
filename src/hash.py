import hashlib


def hash_password(password: str) -> str:
    """Return the SHA‑512 hex digest of the supplied password.

    The original implementation used SHA‑256, but the tests now expect
    a stronger hash.  Switching to SHA‑512 keeps the API unchanged while
    providing the requested security level.
    """
    return hashlib.sha512(password.encode()).hexdigest()

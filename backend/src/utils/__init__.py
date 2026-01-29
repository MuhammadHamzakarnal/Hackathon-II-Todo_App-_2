"""
Utils package - contains utility modules for the application.

IMPORTANT: bcrypt_fix must be imported FIRST before any other modules
that might use passlib or bcrypt to ensure compatibility with bcrypt 4.1+
"""

# Import bcrypt_fix first to apply the compatibility patch
from . import bcrypt_fix  # noqa: F401

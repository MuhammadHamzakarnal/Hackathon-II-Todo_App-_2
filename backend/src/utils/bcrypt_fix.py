"""
Initialization module to fix bcrypt compatibility issue before any other imports

Note: This fix is a fallback. The primary fix is in auth_service.py which applies
the bcrypt fix BEFORE importing passlib. This module provides an additional safety
net when imported early in the application startup.

bcrypt 4.1.0+ removed the __about__ module that passlib uses for version detection,
causing AttributeError. The fix creates a mock __about__ module.
"""

import logging
import sys
import types

logger = logging.getLogger(__name__)

# Apply bcrypt compatibility fix before importing passlib, if needed
try:
    import bcrypt
    if not hasattr(bcrypt, '__about__'):
        logger.info(f"[bcrypt_fix] Applying fix for bcrypt {getattr(bcrypt, '__version__', 'unknown')}")
        bcrypt_about = types.ModuleType('bcrypt.__about__')
        setattr(bcrypt_about, '__version__', getattr(bcrypt, '__version__', '4.0.1'))
        sys.modules['bcrypt.__about__'] = bcrypt_about
        bcrypt.__about__ = bcrypt_about
    else:
        logger.debug(f"[bcrypt_fix] bcrypt.__about__ already exists")
except ImportError:
    logger.error("[bcrypt_fix] Could not import bcrypt - make sure it's installed")
except Exception as e:
    logger.error(f"[bcrypt_fix] Unexpected error: {e}")

# Now safe to import passlib and other modules that depend on bcrypt

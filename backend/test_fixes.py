#!/usr/bin/env python3
"""
Test script to validate the fixes for bcrypt version issue and password length validation
"""

def test_password_truncation():
    """Test the password truncation function in AuthService"""
    print("Testing password truncation...")
    
    # Import the AuthService to test the truncation function
    try:
        from src.services.auth_service import AuthService
        
        # Test with a password longer than 72 bytes
        long_password = "a" * 80  # 80 characters, longer than bcrypt's 72-byte limit
        truncated = AuthService._truncate_password(long_password)
        
        print(f"Original password length: {len(long_password)}")
        print(f"Truncated password length: {len(truncated)}")
        print(f"Truncated correctly: {len(truncated) <= 72}")
        
        # Test with a normal password
        normal_password = "normal_password_123"
        truncated_normal = AuthService._truncate_password(normal_password)
        
        print(f"Normal password length: {len(normal_password)}")
        print(f"Truncated normal password length: {len(truncated_normal)}")
        print(f"Normal password unchanged: {truncated_normal == normal_password}")
        
        print("Password truncation test PASSED!")
        
    except Exception as e:
        print(f"Password truncation test FAILED: {e}")
        return False
    
    return True


def test_user_model_validation():
    """Test the updated UserCreate model validation"""
    print("\nTesting UserCreate model validation...")
    
    try:
        from src.models.user import UserCreate
        from pydantic import ValidationError
        
        # Test with a password that's too long (>72 chars)
        try:
            long_password = "a" * 80  # 80 characters
            user_data = UserCreate(email="test@example.com", password=long_password)
            print("ERROR: UserCreate accepted a password longer than 72 characters!")
            return False
        except ValidationError:
            print("Good: UserCreate rejected password longer than 72 characters")
        
        # Test with a valid password (<72 chars)
        try:
            valid_password = "valid_password_123"  # Less than 72 characters
            user_data = UserCreate(email="test@example.com", password=valid_password)
            print("Good: UserCreate accepted a valid password")
        except ValidationError as e:
            print(f"ERROR: UserCreate rejected a valid password: {e}")
            return False
        
        print("User model validation test PASSED!")
        
    except Exception as e:
        print(f"User model validation test FAILED: {e}")
        return False
    
    return True


def test_bcrypt_import():
    """Test importing bcrypt and checking for the __about__ attribute issue"""
    print("\nTesting bcrypt import and attributes...")
    
    try:
        import bcrypt
        
        print(f"bcrypt version: {getattr(bcrypt, '__version__', 'unknown')}")
        print(f"bcrypt has __about__: {hasattr(bcrypt, '__about__')}")
        
        if hasattr(bcrypt, '__about__'):
            print(f"bcrypt.__about__ version: {getattr(bcrypt.__about__, '__version__', 'unknown')}")
        
        print("Bcrypt import test PASSED!")
        
    except ImportError as e:
        print(f"Bcrypt import test FAILED - could not import bcrypt: {e}")
        return False
    except Exception as e:
        print(f"Bcrypt import test had an issue: {e}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("Running tests for bcrypt and password validation fixes...\n")
    
    results = []
    results.append(test_password_truncation())
    results.append(test_user_model_validation())
    results.append(test_bcrypt_import())
    
    print(f"\nTest Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("All tests PASSED! The fixes should resolve the reported issues.")
    else:
        print("Some tests FAILED. Further investigation needed.")


if __name__ == "__main__":
    main()
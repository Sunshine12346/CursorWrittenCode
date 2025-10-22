#!/usr/bin/env python3
"""
Setup script for Educational Encryption Tools
This script checks and installs the required dependencies.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is 3.7 or higher."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_and_install_package(package_name, import_name=None):
    """Check if a package is installed, and install if not."""
    if import_name is None:
        import_name = package_name
    
    # Check if package is already installed
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        print(f"✅ {package_name} is already installed")
        return True
    
    # Try to install the package
    print(f"📦 Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def test_encryption_tools():
    """Test that the encryption tools can be imported and run."""
    try:
        # Test basic functionality
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        cipher = Fernet(key)
        test_data = b"Hello, World!"
        encrypted = cipher.encrypt(test_data)
        decrypted = cipher.decrypt(encrypted)
        
        if decrypted == test_data:
            print("✅ Cryptography library test passed")
            return True
        else:
            print("❌ Cryptography library test failed")
            return False
    except Exception as e:
        print(f"❌ Cryptography test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🔧 Setting up Educational Encryption Tools")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check and install required packages
    packages = [
        ("cryptography", "cryptography"),
    ]
    
    all_installed = True
    for package_name, import_name in packages:
        if not check_and_install_package(package_name, import_name):
            all_installed = False
    
    if not all_installed:
        print("\n❌ Setup failed: Some packages could not be installed")
        return False
    
    # Test the tools
    print("\n🧪 Testing encryption functionality...")
    if not test_encryption_tools():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nYou can now use the encryption tools:")
    print("  python modern_encrypt.py --help")
    print("  python modern_decrypt.py --help")
    print("\nOn Windows, you can also use:")
    print("  encrypt.bat")
    print("  decrypt.bat")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
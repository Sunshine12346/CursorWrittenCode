#!/usr/bin/env python3
"""
Educational File Encryption Tool
WARNING: This is for educational purposes only!
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Set
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('encryption.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EducationalEncryptor:
    """Educational file encryption class with modern security practices."""
    
    def __init__(self, target_directory: str = ".", password: str = None):
        self.target_directory = Path(target_directory).resolve()
        self.key_file = self.target_directory / "secret.key"
        self.salt_file = self.target_directory / "salt.key"
        self.excluded_files = {
            "modern_encrypt.py", 
            "modern_decrypt.py", 
            "secret.key", 
            "salt.key",
            "encryption.log",
            "nothing.py",
            "decrypt.py"
        }
        self.excluded_extensions = {".log", ".tmp", ".bak"}
        
        if password:
            self.key = self._derive_key_from_password(password)
        else:
            self.key = Fernet.generate_key()
            self._save_key()
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        # Generate or load salt
        if self.salt_file.exists():
            with open(self.salt_file, "rb") as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _save_key(self) -> None:
        """Save the encryption key securely."""
        try:
            with open(self.key_file, "wb") as f:
                f.write(self.key)
            # Set restrictive permissions (owner read/write only)
            os.chmod(self.key_file, 0o600)
            logger.info(f"Key saved to {self.key_file}")
        except Exception as e:
            logger.error(f"Failed to save key: {e}")
            raise
    
    def _should_encrypt_file(self, file_path: Path) -> bool:
        """Determine if a file should be encrypted."""
        if file_path.name in self.excluded_files:
            return False
        if file_path.suffix in self.excluded_extensions:
            return False
        if file_path.is_symlink():
            return False
        if not file_path.is_file():
            return False
        if file_path.stat().st_size == 0:
            logger.warning(f"Skipping empty file: {file_path}")
            return False
        return True
    
    def _get_files_to_encrypt(self, recursive: bool = True) -> List[Path]:
        """Get list of files to encrypt."""
        files = []
        
        if recursive:
            # Recursively find all files
            for root, dirs, filenames in os.walk(self.target_directory):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for filename in filenames:
                    file_path = Path(root) / filename
                    if self._should_encrypt_file(file_path):
                        files.append(file_path)
        else:
            # Only files in current directory
            for item in self.target_directory.iterdir():
                if self._should_encrypt_file(item):
                    files.append(item)
        
        return files
    
    def encrypt_file(self, file_path: Path) -> bool:
        """Encrypt a single file."""
        try:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            
            with open(file_path, "rb") as f:
                contents = f.read()
            
            # Encrypt contents
            fernet = Fernet(self.key)
            encrypted_contents = fernet.encrypt(contents)
            
            # Write encrypted contents
            with open(file_path, "wb") as f:
                f.write(encrypted_contents)
            
            # Remove backup if encryption successful
            if backup_path.exists():
                backup_path.unlink()
            
            logger.info(f"Encrypted: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to encrypt {file_path}: {e}")
            # Restore from backup if it exists
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if backup_path.exists():
                backup_path.rename(file_path)
            return False
    
    def encrypt_directory(self, recursive: bool = True, dry_run: bool = False) -> None:
        """Encrypt all files in the target directory."""
        files_to_encrypt = self._get_files_to_encrypt(recursive)
        
        if not files_to_encrypt:
            logger.info("No files found to encrypt.")
            return
        
        logger.info(f"Found {len(files_to_encrypt)} files to encrypt")
        
        if dry_run:
            logger.info("DRY RUN - Files that would be encrypted:")
            for file_path in files_to_encrypt:
                logger.info(f"  {file_path}")
            return
        
        # Confirm before proceeding
        print(f"\n⚠️  WARNING: This will encrypt {len(files_to_encrypt)} files!")
        print("Files to be encrypted:")
        for file_path in files_to_encrypt[:10]:  # Show first 10
            print(f"  {file_path}")
        if len(files_to_encrypt) > 10:
            print(f"  ... and {len(files_to_encrypt) - 10} more files")
        
        confirm = input("\nDo you want to continue? (type 'YES' to confirm): ")
        if confirm != "YES":
            logger.info("Operation cancelled by user.")
            return
        
        success_count = 0
        for file_path in files_to_encrypt:
            if self.encrypt_file(file_path):
                success_count += 1
        
        logger.info(f"Encryption complete! {success_count}/{len(files_to_encrypt)} files encrypted successfully.")
        print(f"\n🔒 ENCRYPTION COMPLETE!")
        print(f"📁 Directory: {self.target_directory}")
        print(f"✅ Successfully encrypted: {success_count}/{len(files_to_encrypt)} files")
        print(f"🔑 Key saved to: {self.key_file}")
        print(f"\n⚠️  Keep the key file safe - you'll need it to decrypt your files!")

def main():
    parser = argparse.ArgumentParser(
        description="Educational File Encryption Tool",
        epilog="WARNING: This is for educational purposes only!"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Target directory to encrypt (default: current directory)"
    )
    parser.add_argument(
        "--password", "-p",
        help="Use password-based encryption instead of random key"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        default=True,
        help="Recursively encrypt subdirectories (default: True)"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only encrypt files in target directory, not subdirectories"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be encrypted without actually doing it"
    )
    
    args = parser.parse_args()
    
    # Handle recursive flag
    recursive = args.recursive and not args.no_recursive
    
    try:
        # Initialize encryptor
        encryptor = EducationalEncryptor(
            target_directory=args.directory,
            password=args.password
        )
        
        # Perform encryption
        encryptor.encrypt_directory(recursive=recursive, dry_run=args.dry_run)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
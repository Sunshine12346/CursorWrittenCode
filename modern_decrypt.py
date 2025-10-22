#!/usr/bin/env python3
"""
Educational File Decryption Tool
WARNING: This is for educational purposes only!
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import List
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('decryption.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EducationalDecryptor:
    """Educational file decryption class with modern security practices."""
    
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
            "decryption.log",
            "nothing.py",
            "decrypt.py"
        }
        self.excluded_extensions = {".log", ".tmp", ".bak"}
        
        if password:
            self.key = self._derive_key_from_password(password)
        else:
            self.key = self._load_key()
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive decryption key from password using PBKDF2."""
        if not self.salt_file.exists():
            raise FileNotFoundError(f"Salt file not found: {self.salt_file}")
        
        with open(self.salt_file, "rb") as f:
            salt = f.read()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _load_key(self) -> bytes:
        """Load the encryption key from file."""
        if not self.key_file.exists():
            raise FileNotFoundError(f"Key file not found: {self.key_file}")
        
        try:
            with open(self.key_file, "rb") as f:
                key = f.read()
            logger.info(f"Key loaded from {self.key_file}")
            return key
        except Exception as e:
            logger.error(f"Failed to load key: {e}")
            raise
    
    def _is_encrypted_file(self, file_path: Path) -> bool:
        """Check if a file appears to be encrypted."""
        try:
            with open(file_path, "rb") as f:
                # Read first few bytes to check if it looks like Fernet encrypted data
                header = f.read(100)
                
            # Fernet encrypted data starts with gAAAAAB (base64 encoded)
            # This is a heuristic check
            if header.startswith(b'gAAAAAB'):
                return True
                
            # Alternative: try to decrypt a small portion to verify
            try:
                fernet = Fernet(self.key)
                fernet.decrypt(header)
                return True
            except InvalidToken:
                return False
                
        except Exception:
            return False
    
    def _should_decrypt_file(self, file_path: Path) -> bool:
        """Determine if a file should be decrypted."""
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
        return self._is_encrypted_file(file_path)
    
    def _get_files_to_decrypt(self, recursive: bool = True) -> List[Path]:
        """Get list of files to decrypt."""
        files = []
        
        if recursive:
            # Recursively find all encrypted files
            for root, dirs, filenames in os.walk(self.target_directory):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for filename in filenames:
                    file_path = Path(root) / filename
                    if self._should_decrypt_file(file_path):
                        files.append(file_path)
        else:
            # Only files in current directory
            for item in self.target_directory.iterdir():
                if self._should_decrypt_file(item):
                    files.append(item)
        
        return files
    
    def decrypt_file(self, file_path: Path) -> bool:
        """Decrypt a single file."""
        try:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + ".enc_bak")
            
            with open(file_path, "rb") as f:
                encrypted_contents = f.read()
            
            # Create backup of encrypted file
            with open(backup_path, "wb") as f:
                f.write(encrypted_contents)
            
            # Decrypt contents
            fernet = Fernet(self.key)
            decrypted_contents = fernet.decrypt(encrypted_contents)
            
            # Write decrypted contents
            with open(file_path, "wb") as f:
                f.write(decrypted_contents)
            
            # Remove backup if decryption successful
            if backup_path.exists():
                backup_path.unlink()
            
            logger.info(f"Decrypted: {file_path}")
            return True
            
        except InvalidToken:
            logger.error(f"Invalid key or corrupted file: {file_path}")
            # Restore from backup
            backup_path = file_path.with_suffix(file_path.suffix + ".enc_bak")
            if backup_path.exists():
                backup_path.rename(file_path)
            return False
        except Exception as e:
            logger.error(f"Failed to decrypt {file_path}: {e}")
            # Restore from backup
            backup_path = file_path.with_suffix(file_path.suffix + ".enc_bak")
            if backup_path.exists():
                backup_path.rename(file_path)
            return False
    
    def decrypt_directory(self, recursive: bool = True, dry_run: bool = False) -> None:
        """Decrypt all encrypted files in the target directory."""
        files_to_decrypt = self._get_files_to_decrypt(recursive)
        
        if not files_to_decrypt:
            logger.info("No encrypted files found to decrypt.")
            return
        
        logger.info(f"Found {len(files_to_decrypt)} encrypted files to decrypt")
        
        if dry_run:
            logger.info("DRY RUN - Files that would be decrypted:")
            for file_path in files_to_decrypt:
                logger.info(f"  {file_path}")
            return
        
        # Show files to be decrypted
        print(f"\n🔓 Found {len(files_to_decrypt)} encrypted files:")
        for file_path in files_to_decrypt[:10]:  # Show first 10
            print(f"  {file_path}")
        if len(files_to_decrypt) > 10:
            print(f"  ... and {len(files_to_decrypt) - 10} more files")
        
        confirm = input("\nDo you want to decrypt these files? (type 'YES' to confirm): ")
        if confirm != "YES":
            logger.info("Operation cancelled by user.")
            return
        
        success_count = 0
        for file_path in files_to_decrypt:
            if self.decrypt_file(file_path):
                success_count += 1
        
        logger.info(f"Decryption complete! {success_count}/{len(files_to_decrypt)} files decrypted successfully.")
        print(f"\n🔓 DECRYPTION COMPLETE!")
        print(f"📁 Directory: {self.target_directory}")
        print(f"✅ Successfully decrypted: {success_count}/{len(files_to_decrypt)} files")
        
        if success_count == len(files_to_decrypt):
            print(f"\n🎉 All files have been successfully decrypted!")
        else:
            print(f"\n⚠️  {len(files_to_decrypt) - success_count} files could not be decrypted.")
            print("Check the log for details.")

def main():
    parser = argparse.ArgumentParser(
        description="Educational File Decryption Tool",
        epilog="WARNING: This is for educational purposes only!"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Target directory to decrypt (default: current directory)"
    )
    parser.add_argument(
        "--password", "-p",
        help="Use password-based decryption"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        default=True,
        help="Recursively decrypt subdirectories (default: True)"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only decrypt files in target directory, not subdirectories"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be decrypted without actually doing it"
    )
    
    args = parser.parse_args()
    
    # Handle recursive flag
    recursive = args.recursive and not args.no_recursive
    
    try:
        # Initialize decryptor
        decryptor = EducationalDecryptor(
            target_directory=args.directory,
            password=args.password
        )
        
        # Perform decryption
        decryptor.decrypt_directory(recursive=recursive, dry_run=args.dry_run)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"Required file not found: {e}")
        print(f"\n❌ Error: {e}")
        print("Make sure you have the key file (secret.key) or salt file (salt.key) if using password.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
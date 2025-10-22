#!/usr/bin/env python3
"""
Enhanced Educational File Decryption Tool
WARNING: This is for educational purposes only!

Enhanced features:
- Flexible key storage locations
- Better remote directory support
- Automatic key discovery
- Advanced file detection
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Optional
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json

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

class EnhancedDecryptor:
    """Enhanced educational file decryption class with advanced features."""
    
    def __init__(self, target_directory: str = ".", password: str = None, 
                 key_storage_dir: str = None, config_file: str = None):
        self.target_directory = Path(target_directory).resolve()
        
        # Flexible key storage - can be different from target directory
        if key_storage_dir:
            self.key_storage_dir = Path(key_storage_dir).resolve()
        else:
            self.key_storage_dir = self.target_directory
            
        self.key_file = self.key_storage_dir / "secret.key"
        self.salt_file = self.key_storage_dir / "salt.key"
        self.config_file = self.key_storage_dir / (config_file or "encryption_config.json")
        
        # Default exclusions
        self.excluded_files = {
            "modern_encrypt.py", 
            "modern_decrypt.py", 
            "enhanced_encrypt.py",
            "enhanced_decrypt.py",
            "secret.key", 
            "salt.key",
            "encryption.log",
            "decryption.log",
            "encryption_config.json",
            "nothing.py",
            "decrypt.py"
        }
        self.excluded_extensions = {".log", ".tmp", ".bak", ".enc_bak"}
        
        # Load configuration if exists
        self._load_config()
        
        # Initialize decryption
        if password:
            self.key = self._derive_key_from_password(password)
        else:
            self.key = self._load_key()
    
    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Load exclusions
                if 'excluded_files' in config:
                    self.excluded_files.update(config['excluded_files'])
                if 'excluded_extensions' in config:
                    self.excluded_extensions.update(config['excluded_extensions'])
                    
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive decryption key from password using PBKDF2."""
        # Try to find salt file in multiple locations
        salt_locations = [
            self.salt_file,
            self.target_directory / "salt.key",
            Path(".") / "salt.key"
        ]
        
        salt_file_found = None
        for salt_path in salt_locations:
            if salt_path.exists():
                salt_file_found = salt_path
                break
        
        if not salt_file_found:
            raise FileNotFoundError(f"Salt file not found in any of these locations: {[str(p) for p in salt_locations]}")
        
        with open(salt_file_found, "rb") as f:
            salt = f.read()
        
        logger.info(f"Using salt file: {salt_file_found}")
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _load_key(self) -> bytes:
        """Load the encryption key from file with multiple location search."""
        # Try to find key file in multiple locations
        key_locations = [
            self.key_file,
            self.target_directory / "secret.key",
            Path(".") / "secret.key"
        ]
        
        key_file_found = None
        for key_path in key_locations:
            if key_path.exists():
                key_file_found = key_path
                break
        
        if not key_file_found:
            print(f"\n❌ Key file not found in any of these locations:")
            for location in key_locations:
                print(f"   - {location}")
            print(f"\n💡 Solutions:")
            print(f"   1. Make sure you have the 'secret.key' file")
            print(f"   2. Use --key-storage-dir to specify where your keys are stored")
            print(f"   3. Use --password if you used password-based encryption")
            print(f"   4. Copy the key file to one of the expected locations")
            raise FileNotFoundError(f"Key file not found in any expected location")
        
        try:
            with open(key_file_found, "rb") as f:
                key = f.read()
            logger.info(f"Key loaded from {key_file_found}")
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
            if header.startswith(b'gAAAAAB'):
                return True
                
            # Alternative: try to decrypt a small portion to verify
            try:
                fernet = Fernet(self.key)
                # Try to decrypt just the first part to verify it's encrypted
                test_data = header[:100] if len(header) >= 100 else header
                fernet.decrypt(test_data)
                return True
            except (InvalidToken, Exception):
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
        
        if not self.target_directory.exists():
            logger.error(f"Target directory does not exist: {self.target_directory}")
            return files
        
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
    
    def decrypt_multiple_directories(self, directories: List[str], 
                                   recursive: bool = True, dry_run: bool = False) -> None:
        """Decrypt files in multiple directories."""
        all_files = []
        
        for directory in directories:
            self.target_directory = Path(directory).resolve()
            files = self._get_files_to_decrypt(recursive)
            all_files.extend(files)
            logger.info(f"Found {len(files)} encrypted files in {directory}")
        
        if not all_files:
            logger.info("No encrypted files found to decrypt in any directory.")
            return
        
        self._process_files(all_files, dry_run, "decrypt")
    
    def decrypt_directory(self, recursive: bool = True, dry_run: bool = False) -> None:
        """Decrypt all encrypted files in the target directory."""
        files_to_decrypt = self._get_files_to_decrypt(recursive)
        
        if not files_to_decrypt:
            logger.info("No encrypted files found to decrypt.")
            print(f"\n🔍 No encrypted files found in: {self.target_directory}")
            print(f"📁 Searched directory: {self.target_directory}")
            print(f"🔑 Using keys from: {self.key_storage_dir}")
            print(f"\n💡 This could mean:")
            print(f"   - Files are not encrypted")
            print(f"   - Wrong key/password")
            print(f"   - Files encrypted with different tool")
            return
        
        self._process_files(files_to_decrypt, dry_run, "decrypt")
    
    def _process_files(self, files: List[Path], dry_run: bool, operation: str) -> None:
        """Process files for decryption."""
        logger.info(f"Found {len(files)} files to {operation}")
        
        if dry_run:
            logger.info(f"DRY RUN - Files that would be {operation}ed:")
            for file_path in files:
                logger.info(f"  {file_path}")
            return
        
        # Show file summary
        print(f"\n🔓 Found {len(files)} encrypted files to {operation}:")
        print(f"📁 Target directory: {self.target_directory}")
        print(f"🔑 Using keys from: {self.key_storage_dir}")
        
        # Group files by directory for better display
        dirs = {}
        for file_path in files:
            dir_path = file_path.parent
            if dir_path not in dirs:
                dirs[dir_path] = []
            dirs[dir_path].append(file_path.name)
        
        for dir_path, filenames in list(dirs.items())[:5]:  # Show first 5 directories
            print(f"  📂 {dir_path}:")
            for filename in filenames[:3]:  # Show first 3 files per directory
                print(f"    📄 {filename}")
            if len(filenames) > 3:
                print(f"    ... and {len(filenames) - 3} more files")
        
        if len(dirs) > 5:
            total_remaining = len(files) - sum(len(filenames) for filenames in list(dirs.values())[:5])
            print(f"  ... and {len(dirs) - 5} more directories with {total_remaining} files")
        
        confirm = input(f"\nDo you want to {operation} these files? (type 'YES' to confirm): ")
        if confirm != "YES":
            logger.info("Operation cancelled by user.")
            return
        
        success_count = 0
        for file_path in files:
            if self.decrypt_file(file_path):
                success_count += 1
        
        logger.info(f"Decryption complete! {success_count}/{len(files)} files decrypted successfully.")
        print(f"\n🔓 DECRYPTION COMPLETE!")
        print(f"📁 Target directory: {self.target_directory}")
        print(f"🔑 Keys used from: {self.key_storage_dir}")
        print(f"✅ Successfully decrypted: {success_count}/{len(files)} files")
        
        if success_count == len(files):
            print(f"\n🎉 All files have been successfully decrypted!")
        else:
            print(f"\n⚠️  {len(files) - success_count} files could not be decrypted.")
            print("Check the log for details.")

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Educational File Decryption Tool",
        epilog="WARNING: This is for educational purposes only!"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Target directory to decrypt (default: current directory)"
    )
    parser.add_argument(
        "--multiple-dirs", "-m",
        nargs="+",
        help="Decrypt multiple directories"
    )
    parser.add_argument(
        "--key-storage-dir", "-k",
        help="Directory where keys are stored (default: search multiple locations)"
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
        "--config-file",
        help="Configuration file name (default: encryption_config.json)"
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
        decryptor = EnhancedDecryptor(
            target_directory=args.directory,
            password=args.password,
            key_storage_dir=args.key_storage_dir,
            config_file=args.config_file
        )
        
        # Perform decryption
        if args.multiple_dirs:
            decryptor.decrypt_multiple_directories(
                directories=args.multiple_dirs,
                recursive=recursive,
                dry_run=args.dry_run
            )
        else:
            decryptor.decrypt_directory(recursive=recursive, dry_run=args.dry_run)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"Required file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Enhanced Educational File Encryption Tool
WARNING: This is for educational purposes only!

Enhanced features:
- Flexible key storage locations
- Better remote directory support
- Multiple target directories
- Advanced exclusion patterns
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Set, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
from datetime import datetime

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

class EnhancedEncryptor:
    """Enhanced educational file encryption class with advanced features."""
    
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
        self.excluded_patterns = set()  # For regex patterns
        
        # Load configuration if exists
        self._load_config()
        
        # Initialize encryption
        if password:
            self.key = self._derive_key_from_password(password)
        else:
            self.key = Fernet.generate_key()
            self._save_key()
            
        # Save current configuration
        self._save_config()
    
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
                if 'excluded_patterns' in config:
                    self.excluded_patterns.update(config['excluded_patterns'])
                    
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
    
    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            # Ensure key storage directory exists
            self.key_storage_dir.mkdir(parents=True, exist_ok=True)
            
            config = {
                'target_directory': str(self.target_directory),
                'key_storage_dir': str(self.key_storage_dir),
                'excluded_files': list(self.excluded_files),
                'excluded_extensions': list(self.excluded_extensions),
                'excluded_patterns': list(self.excluded_patterns),
                'created_at': datetime.now().isoformat(),
                'tool_version': '2.0'
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.warning(f"Failed to save config: {e}")
    
    def add_exclusion_pattern(self, pattern: str) -> None:
        """Add a regex pattern to exclude files."""
        self.excluded_patterns.add(pattern)
        logger.info(f"Added exclusion pattern: {pattern}")
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        # Ensure key storage directory exists
        self.key_storage_dir.mkdir(parents=True, exist_ok=True)
        
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
            # Ensure key storage directory exists
            self.key_storage_dir.mkdir(parents=True, exist_ok=True)
            
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
        # Check excluded files
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
            
        # Check regex patterns
        import re
        for pattern in self.excluded_patterns:
            try:
                if re.search(pattern, str(file_path)):
                    logger.info(f"Skipping file matching pattern '{pattern}': {file_path}")
                    return False
            except re.error:
                logger.warning(f"Invalid regex pattern: {pattern}")
                
        return True
    
    def _get_files_to_encrypt(self, recursive: bool = True) -> List[Path]:
        """Get list of files to encrypt."""
        files = []
        
        if not self.target_directory.exists():
            logger.error(f"Target directory does not exist: {self.target_directory}")
            return files
        
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
    
    def encrypt_multiple_directories(self, directories: List[str], 
                                   recursive: bool = True, dry_run: bool = False) -> None:
        """Encrypt files in multiple directories."""
        all_files = []
        
        for directory in directories:
            self.target_directory = Path(directory).resolve()
            files = self._get_files_to_encrypt(recursive)
            all_files.extend(files)
            logger.info(f"Found {len(files)} files in {directory}")
        
        if not all_files:
            logger.info("No files found to encrypt in any directory.")
            return
        
        self._process_files(all_files, dry_run, "encrypt")
    
    def encrypt_directory(self, recursive: bool = True, dry_run: bool = False) -> None:
        """Encrypt all files in the target directory."""
        files_to_encrypt = self._get_files_to_encrypt(recursive)
        
        if not files_to_encrypt:
            logger.info("No files found to encrypt.")
            return
        
        self._process_files(files_to_encrypt, dry_run, "encrypt")
    
    def _process_files(self, files: List[Path], dry_run: bool, operation: str) -> None:
        """Process files for encryption."""
        logger.info(f"Found {len(files)} files to {operation}")
        
        if dry_run:
            logger.info(f"DRY RUN - Files that would be {operation}ed:")
            for file_path in files:
                logger.info(f"  {file_path}")
            return
        
        # Show file summary
        print(f"\n🔒 Found {len(files)} files to {operation}:")
        print(f"📁 Target directory: {self.target_directory}")
        print(f"🔑 Keys stored in: {self.key_storage_dir}")
        
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
            if self.encrypt_file(file_path):
                success_count += 1
        
        logger.info(f"Encryption complete! {success_count}/{len(files)} files encrypted successfully.")
        print(f"\n🔒 ENCRYPTION COMPLETE!")
        print(f"📁 Target directory: {self.target_directory}")
        print(f"🔑 Keys stored in: {self.key_storage_dir}")
        print(f"✅ Successfully encrypted: {success_count}/{len(files)} files")
        print(f"\n⚠️  Key files location: {self.key_storage_dir}")
        print("Keep these files safe - you'll need them to decrypt your files!")

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Educational File Encryption Tool",
        epilog="WARNING: This is for educational purposes only!"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Target directory to encrypt (default: current directory)"
    )
    parser.add_argument(
        "--multiple-dirs", "-m",
        nargs="+",
        help="Encrypt multiple directories"
    )
    parser.add_argument(
        "--key-storage-dir", "-k",
        help="Directory to store keys (default: same as target directory)"
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
        "--exclude-pattern",
        action="append",
        help="Add regex pattern to exclude files (can be used multiple times)"
    )
    parser.add_argument(
        "--config-file",
        help="Configuration file name (default: encryption_config.json)"
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
        encryptor = EnhancedEncryptor(
            target_directory=args.directory,
            password=args.password,
            key_storage_dir=args.key_storage_dir,
            config_file=args.config_file
        )
        
        # Add exclusion patterns
        if args.exclude_pattern:
            for pattern in args.exclude_pattern:
                encryptor.add_exclusion_pattern(pattern)
        
        # Perform encryption
        if args.multiple_dirs:
            encryptor.encrypt_multiple_directories(
                directories=args.multiple_dirs,
                recursive=recursive,
                dry_run=args.dry_run
            )
        else:
            encryptor.encrypt_directory(recursive=recursive, dry_run=args.dry_run)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
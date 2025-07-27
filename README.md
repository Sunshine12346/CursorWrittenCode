# Educational Encryption/Decryption Tools

⚠️ **WARNING: These tools are for educational purposes only!** ⚠️

Modern, robust file encryption and decryption tools built with Python and the `cryptography` library. These tools demonstrate proper cryptographic practices and include comprehensive safety features.

## Features

### 🔒 Modern Encryption (`modern_encrypt.py`)
- **Strong Encryption**: Uses Fernet (AES 128 in CBC mode with HMAC for authentication)
- **Password Support**: Option to use password-based encryption with PBKDF2 (100,000 iterations)
- **Directory Support**: Can encrypt entire directory trees recursively
- **Safety Features**: 
  - File backups during encryption
  - User confirmation before proceeding
  - Dry-run mode to preview actions
  - Comprehensive logging
  - Excludes system/important files automatically

### 🔓 Modern Decryption (`modern_decrypt.py`)
- **Smart Detection**: Automatically detects encrypted files
- **Error Recovery**: Restores files from backups if decryption fails
- **Verification**: Validates encryption before attempting decryption
- **Comprehensive Logging**: Detailed logs of all operations

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Encryption
```bash
# Encrypt current directory (recursive by default)
python modern_encrypt.py

# Encrypt specific directory
python modern_encrypt.py --directory /path/to/target

# Use password-based encryption
python modern_encrypt.py --password mypassword

# Dry run (see what would be encrypted)
python modern_encrypt.py --dry-run
```

### Basic Decryption
```bash
# Decrypt current directory
python modern_decrypt.py

# Decrypt specific directory
python modern_decrypt.py --directory /path/to/target

# Use password-based decryption
python modern_decrypt.py --password mypassword

# Dry run (see what would be decrypted)
python modern_decrypt.py --dry-run
```

### Advanced Options

#### Encryption Options
- `--directory, -d`: Target directory (default: current directory)
- `--password, -p`: Use password-based encryption
- `--recursive, -r`: Recursively encrypt subdirectories (default: True)
- `--no-recursive`: Only encrypt files in target directory
- `--dry-run`: Preview what would be encrypted

#### Decryption Options
- `--directory, -d`: Target directory (default: current directory)
- `--password, -p`: Use password-based decryption
- `--recursive, -r`: Recursively decrypt subdirectories (default: True)
- `--no-recursive`: Only decrypt files in target directory
- `--dry-run`: Preview what would be decrypted

### Examples

```bash
# Encrypt a specific folder with password
python modern_encrypt.py -d /home/user/documents -p mypassword

# Preview encryption (no actual changes)
python modern_encrypt.py --dry-run

# Encrypt only current directory (no subdirectories)
python modern_encrypt.py --no-recursive

# Decrypt with password
python modern_decrypt.py -p mypassword
```

## Security Features

### Encryption Security
- **AES-128 encryption** in CBC mode with HMAC authentication
- **PBKDF2** with 100,000 iterations for password-based keys
- **Random salt generation** for each password-based encryption
- **Secure key generation** using cryptographically secure random numbers

### Safety Features
- **Automatic backups** during encryption/decryption
- **File validation** before processing
- **Error recovery** with backup restoration
- **User confirmation** for destructive operations
- **Comprehensive logging** for audit trails

### File Exclusions
The tools automatically exclude:
- Script files (`modern_encrypt.py`, `modern_decrypt.py`)
- Key files (`secret.key`, `salt.key`)
- Log files (`*.log`)
- Temporary files (`*.tmp`, `*.bak`)
- Hidden directories (`.git`, `.vscode`, etc.)

## File Structure

After encryption, you'll have:
- `secret.key` - Encryption key (for random key mode)
- `salt.key` - Salt file (for password mode)
- `encryption.log` - Detailed operation log
- `decryption.log` - Decryption operation log

## Important Notes

### ⚠️ Security Warnings
1. **Keep your key files safe!** Without them, your files cannot be decrypted
2. **Use strong passwords** if using password-based encryption
3. **This is for education only** - not for protecting sensitive real-world data
4. **Test thoroughly** before using on important files

### 🔒 Key Management
- **Random Key Mode**: Key is saved to `secret.key` - keep this file safe!
- **Password Mode**: Salt is saved to `salt.key` - keep both password and salt safe!
- Keys are saved with restrictive permissions (600) for security

### 🚫 What Gets Excluded
- The encryption/decryption scripts themselves
- Key and salt files
- Log files
- Backup files (`.bak`, `.tmp`)
- Empty files
- Symbolic links
- Hidden directories

## Troubleshooting

### Common Issues

**"Key file not found"**
- Make sure `secret.key` exists in the target directory
- If using password mode, ensure `salt.key` exists

**"Invalid key or corrupted file"**
- Wrong password or key
- File may be corrupted
- File might not be encrypted with this tool

**"Permission denied"**
- Run with appropriate permissions
- Check file/directory ownership

### Recovery
- Encrypted file backups are created during decryption (`.enc_bak`)
- Original file backups are created during encryption (`.bak`)
- Check logs for detailed error information

## Educational Value

These tools demonstrate:
- Modern cryptographic best practices
- Proper error handling and recovery
- User-friendly security tools design
- Python cryptography library usage
- File system operations and safety

## License

This project is for educational purposes only. Use responsibly and ethically.
# Cross-Platform Educational Encryption Tools

⚠️ **WARNING: These tools are for educational purposes only!** ⚠️

This guide covers usage on both **Linux** and **Windows** platforms with complete examples and troubleshooting.

## 📦 Available Tools

### Core Python Scripts (Cross-platform)
- `modern_encrypt.py` - Modern encryption tool
- `modern_decrypt.py` - Modern decryption tool
- `enhanced_encrypt.py` - Enhanced encryption with advanced features
- `setup.py` - Automated setup and dependency installer

### Platform-Specific Convenience Scripts

#### Linux Scripts
- `encrypt.sh` - Easy encryption for Linux
- `decrypt.sh` - Easy decryption for Linux

#### Windows Scripts
- `encrypt.bat` - Easy encryption for Windows
- `decrypt.bat` - Easy decryption for Windows

## 🚀 Quick Start Guide

### Linux Quick Start

```bash
# 1. Make scripts executable
chmod +x encrypt.sh decrypt.sh

# 2. Run setup (recommended)
python3 setup.py

# 3. Easy encryption using shell script
./encrypt.sh

# 4. Easy decryption using shell script
./decrypt.sh

# 5. Or use Python directly
python3 modern_encrypt.py --help
```

### Windows Quick Start

```cmd
REM 1. Run setup (recommended)
python setup.py

REM 2. Easy encryption using batch file
encrypt.bat

REM 3. Easy decryption using batch file
decrypt.bat

REM 4. Or use Python directly
python modern_encrypt.py --help
```

## 📋 Installation Instructions

### Linux Installation

#### Ubuntu/Debian
```bash
# Install Python3 and pip
sudo apt update
sudo apt install python3 python3-pip

# Install cryptography (choose one method)
# Method 1: Using pip
pip3 install cryptography

# Method 2: Using system package manager
sudo apt install python3-cryptography

# Method 3: Run our setup script
python3 setup.py
```

#### CentOS/RHEL/Fedora
```bash
# Install Python3 and pip
sudo yum install python3 python3-pip
# or for newer versions:
sudo dnf install python3 python3-pip

# Install cryptography
pip3 install cryptography

# Or run setup script
python3 setup.py
```

#### Arch Linux
```bash
# Install Python3 and pip
sudo pacman -S python python-pip

# Install cryptography
pip install cryptography
# or
sudo pacman -S python-cryptography

# Or run setup script
python setup.py
```

### Windows Installation

#### Method 1: Download Python from python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.7+ (make sure to check "Add to PATH")
3. Install Python
4. Open Command Prompt and run:
```cmd
python setup.py
```

#### Method 2: Using Microsoft Store
1. Open Microsoft Store
2. Search for "Python"
3. Install Python 3.x
4. Open Command Prompt and run:
```cmd
python setup.py
```

#### Method 3: Manual Installation
```cmd
pip install cryptography
```

## 🔧 Usage Examples

### Basic Encryption

#### Linux
```bash
# Encrypt current directory
python3 modern_encrypt.py

# Encrypt specific directory
python3 modern_encrypt.py --directory /home/user/documents

# Encrypt with password
python3 modern_encrypt.py --password mypassword

# Encrypt outside directory with key storage elsewhere
python3 enhanced_encrypt.py --directory /tmp/target --key-storage-dir /home/user/keys

# Using convenience script
./encrypt.sh --directory /home/user/documents
```

#### Windows
```cmd
REM Encrypt current directory
python modern_encrypt.py

REM Encrypt specific directory
python modern_encrypt.py --directory "C:\Users\Username\Documents"

REM Encrypt with password
python modern_encrypt.py --password mypassword

REM Encrypt outside directory with key storage elsewhere
python enhanced_encrypt.py --directory "D:\TargetFolder" --key-storage-dir "C:\Keys"

REM Using convenience script
encrypt.bat --directory "C:\Users\Username\Documents"
```

### Advanced Features (Enhanced Tool)

#### Linux
```bash
# Encrypt multiple directories
python3 enhanced_encrypt.py --multiple-dirs /home/user/docs /home/user/photos /tmp/files

# Encrypt with custom exclusion patterns
python3 enhanced_encrypt.py --exclude-pattern ".*\.mp4$" --exclude-pattern ".*\.avi$"

# Store keys in different location
python3 enhanced_encrypt.py --directory /tmp/target --key-storage-dir /home/user/secure_keys

# Preview what would be encrypted
python3 enhanced_encrypt.py --dry-run --directory /home/user/documents
```

#### Windows
```cmd
REM Encrypt multiple directories
python enhanced_encrypt.py --multiple-dirs "C:\Folder1" "C:\Folder2" "D:\Folder3"

REM Encrypt with custom exclusion patterns
python enhanced_encrypt.py --exclude-pattern ".*\.mp4$" --exclude-pattern ".*\.avi$"

REM Store keys in different location
python enhanced_encrypt.py --directory "D:\Target" --key-storage-dir "C:\SecureKeys"

REM Preview what would be encrypted
python enhanced_encrypt.py --dry-run --directory "C:\Users\Username\Documents"
```

### Decryption Examples

#### Linux
```bash
# Decrypt current directory
python3 modern_decrypt.py

# Decrypt specific directory
python3 modern_decrypt.py --directory /home/user/encrypted_docs

# Decrypt with password
python3 modern_decrypt.py --password mypassword

# Using convenience script
./decrypt.sh --password mypassword
```

#### Windows
```cmd
REM Decrypt current directory
python modern_decrypt.py

REM Decrypt specific directory
python modern_decrypt.py --directory "C:\Users\Username\EncryptedDocs"

REM Decrypt with password
python modern_decrypt.py --password mypassword

REM Using convenience script
decrypt.bat --password mypassword
```

## 🌍 Remote Directory Encryption

### Encrypting Files Outside Current Directory

Both tools support encrypting files in any directory on your system:

#### Linux Examples
```bash
# Encrypt files in /tmp, store keys in current directory
python3 modern_encrypt.py --directory /tmp

# Encrypt files in /home/user/documents, store keys in /home/user/keys
python3 enhanced_encrypt.py --directory /home/user/documents --key-storage-dir /home/user/keys

# Encrypt multiple remote directories
python3 enhanced_encrypt.py --multiple-dirs /var/www /home/user/projects /tmp/test

# Encrypt user's home directory (be careful!)
python3 modern_encrypt.py --directory /home/user --dry-run  # Preview first!
```

#### Windows Examples
```cmd
REM Encrypt files in D:\, store keys in current directory
python modern_encrypt.py --directory "D:\"

REM Encrypt files in Documents, store keys elsewhere
python enhanced_encrypt.py --directory "C:\Users\Username\Documents" --key-storage-dir "C:\Keys"

REM Encrypt multiple remote directories
python enhanced_encrypt.py --multiple-dirs "D:\Projects" "E:\Backup" "F:\Data"

REM Encrypt external drive (be careful!)
python modern_encrypt.py --directory "E:\" --dry-run
```

### Key Management for Remote Directories

When encrypting remote directories, you have flexibility in where to store keys:

```bash
# Linux: Store keys in home directory, encrypt external drive
python3 enhanced_encrypt.py \
    --directory /mnt/external_drive \
    --key-storage-dir /home/user/.encryption_keys

# Windows: Store keys in Documents, encrypt D: drive
python enhanced_encrypt.py ^
    --directory "D:\" ^
    --key-storage-dir "C:\Users\Username\Documents\Keys"
```

## 🛠️ Platform-Specific Commands

### Linux-Specific Commands
```bash
# Check Python version
python3 --version

# Check if cryptography is installed
python3 -c "import cryptography; print('✅ Cryptography available')"

# Install using system package manager
sudo apt install python3-cryptography  # Ubuntu/Debian
sudo yum install python3-cryptography  # CentOS/RHEL
sudo pacman -S python-cryptography     # Arch

# Make scripts executable
chmod +x *.sh

# View file permissions
ls -la *.py *.sh

# Check disk space before encryption
df -h

# Monitor encryption progress (in another terminal)
watch -n 1 'ls -la /path/to/target | wc -l'
```

### Windows-Specific Commands
```cmd
REM Check Python version
python --version

REM Check if cryptography is installed
python -c "import cryptography; print('✅ Cryptography available')"

REM List Python packages
pip list

REM Check disk space
dir "C:\" /-c

REM View file attributes
attrib *.py

REM Run as administrator (if needed)
PowerShell -Command "Start-Process cmd -ArgumentList '/c encrypt.bat' -Verb RunAs"
```

## 🔍 Troubleshooting

### Common Linux Issues

**Issue: Permission denied**
```bash
# Solution: Fix permissions
chmod +x encrypt.sh decrypt.sh
chmod 644 *.py

# Or run with sudo (not recommended for encryption tools)
sudo python3 modern_encrypt.py
```

**Issue: Python3 not found**
```bash
# Check if python3 is installed
which python3

# Install Python3
sudo apt install python3        # Ubuntu/Debian
sudo yum install python3        # CentOS/RHEL
sudo pacman -S python          # Arch
```

**Issue: Module not found**
```bash
# Install cryptography
pip3 install --user cryptography

# Or use system package
sudo apt install python3-cryptography
```

### Common Windows Issues

**Issue: 'python' is not recognized**
```cmd
REM Try these alternatives
py modern_encrypt.py
python3 modern_encrypt.py
"C:\Python39\python.exe" modern_encrypt.py

REM Add Python to PATH or reinstall with "Add to PATH" checked
```

**Issue: Access denied**
```cmd
REM Run Command Prompt as Administrator
REM Right-click Command Prompt → "Run as administrator"

REM Or check file permissions
attrib -r *.py
```

**Issue: Path with spaces**
```cmd
REM Use quotes around paths
python modern_encrypt.py --directory "C:\Program Files\MyApp"
```

## 🔒 Security Best Practices

### For Both Platforms

1. **Backup Important Files**
   ```bash
   # Linux
   cp -r /important/data /backup/location
   ```
   ```cmd
   REM Windows
   xcopy "C:\Important\Data" "D:\Backup\" /E /I
   ```

2. **Test with Unimportant Files First**
   ```bash
   # Linux
   mkdir /tmp/test_encryption
   echo "test data" > /tmp/test_encryption/test.txt
   python3 modern_encrypt.py --directory /tmp/test_encryption
   ```
   ```cmd
   REM Windows
   mkdir "C:\Temp\test_encryption"
   echo test data > "C:\Temp\test_encryption\test.txt"
   python modern_encrypt.py --directory "C:\Temp\test_encryption"
   ```

3. **Secure Key Storage**
   ```bash
   # Linux: Store keys in secure location
   mkdir -p ~/.encryption_keys
   chmod 700 ~/.encryption_keys
   ```
   ```cmd
   REM Windows: Store keys in protected location
   mkdir "%USERPROFILE%\EncryptionKeys"
   attrib +h "%USERPROFILE%\EncryptionKeys"
   ```

## 📁 File Structure After Installation

```
your_project_folder/
├── modern_encrypt.py          # Core encryption tool
├── modern_decrypt.py          # Core decryption tool
├── enhanced_encrypt.py        # Advanced encryption tool
├── setup.py                   # Setup script
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── CROSS_PLATFORM_GUIDE.md    # This file
├── WINDOWS_USAGE.md           # Windows-specific guide
├── Linux Scripts:
│   ├── encrypt.sh             # Linux encryption script
│   └── decrypt.sh             # Linux decryption script
├── Windows Scripts:
│   ├── encrypt.bat            # Windows encryption script
│   └── decrypt.bat            # Windows decryption script
└── Test Files:
    └── test_sample.txt        # Sample file for testing
```

## 🎯 Quick Command Reference

### Linux
```bash
# Setup
python3 setup.py

# Easy encryption/decryption
./encrypt.sh
./decrypt.sh

# Direct Python usage
python3 modern_encrypt.py --directory /path/to/target
python3 modern_decrypt.py --directory /path/to/target

# Advanced features
python3 enhanced_encrypt.py --multiple-dirs /dir1 /dir2 /dir3
python3 enhanced_encrypt.py --exclude-pattern ".*\.log$"
```

### Windows
```cmd
REM Setup
python setup.py

REM Easy encryption/decryption
encrypt.bat
decrypt.bat

REM Direct Python usage
python modern_encrypt.py --directory "C:\Path\To\Target"
python modern_decrypt.py --directory "C:\Path\To\Target"

REM Advanced features
python enhanced_encrypt.py --multiple-dirs "C:\Dir1" "C:\Dir2" "C:\Dir3"
python enhanced_encrypt.py --exclude-pattern ".*\.log$"
```

## 📞 Need Help?

1. **Check the logs**: Look at `encryption.log` and `decryption.log`
2. **Use dry-run mode**: Add `--dry-run` to preview operations
3. **Test with small files first**: Always test on unimportant data
4. **Check file permissions**: Ensure you have read/write access to target directories
5. **Verify dependencies**: Run `python3 setup.py` (Linux) or `python setup.py` (Windows)

Remember: These tools are for educational purposes only! Always backup important data before testing encryption tools.
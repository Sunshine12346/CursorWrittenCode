# Windows Usage Guide

## Fixing "Invalid argument" Error

If you're getting an error like:
```
python: can't open file "D:\\path\\to\\modern_encrypt.py": [Errno 22] Invalid argument
```

Here are the solutions:

### Solution 1: Use the Batch Files (Easiest)
Instead of running Python directly, use the provided batch files:

```cmd
# For encryption
encrypt.bat

# For decryption  
decrypt.bat
```

These batch files handle all the setup automatically.

### Solution 2: Use Correct Python Command
Try these commands in order:

```cmd
# Option 1: Use 'python' (most common on Windows)
python modern_encrypt.py --help

# Option 2: Use 'py' (Python Launcher)
py modern_encrypt.py --help

# Option 3: Use full path to Python
"C:\Python39\python.exe" modern_encrypt.py --help
```

### Solution 3: Fix Path Issues
If you have spaces or special characters in your path:

```cmd
# Use quotes around the file path
python "modern_encrypt.py" --help

# Or change to the directory first
cd "D:\Shaunak's CODING!\RANSOMWARE\test2"
python modern_encrypt.py --help
```

### Solution 4: Check File Permissions
Make sure the Python files have the correct permissions:

1. Right-click on `modern_encrypt.py`
2. Select "Properties"
3. Make sure "Read-only" is unchecked
4. Click "OK"

## Quick Start for Windows

1. **Download all files** to a folder (e.g., `C:\encryption_tools\`)

2. **Open Command Prompt** in that folder:
   - Hold Shift + Right-click in the folder
   - Select "Open PowerShell window here" or "Open command window here"

3. **Run setup** (optional but recommended):
   ```cmd
   python setup.py
   ```

4. **Test with dry run**:
   ```cmd
   python modern_encrypt.py --dry-run
   ```

5. **Encrypt files**:
   ```cmd
   python modern_encrypt.py
   ```

6. **Decrypt files**:
   ```cmd
   python modern_decrypt.py
   ```

## Alternative: Using PowerShell

If Command Prompt doesn't work, try PowerShell:

```powershell
# Open PowerShell in the folder
python .\modern_encrypt.py --help
```

## Common Windows Issues

### Issue: Python not found
**Solution**: Install Python from python.org and make sure "Add to PATH" is checked during installation.

### Issue: Permission denied
**Solution**: Run Command Prompt as Administrator or check file permissions.

### Issue: Module not found
**Solution**: Install cryptography:
```cmd
pip install cryptography
```

### Issue: Path with spaces
**Solution**: Use quotes around paths:
```cmd
python modern_encrypt.py --directory "C:\My Documents\Files"
```

## Example Windows Commands

```cmd
# Encrypt current folder
python modern_encrypt.py

# Encrypt with password
python modern_encrypt.py --password mypassword

# Encrypt specific folder
python modern_encrypt.py --directory "C:\Users\YourName\Documents"

# Preview what would be encrypted
python modern_encrypt.py --dry-run

# Decrypt current folder
python modern_decrypt.py

# Decrypt with password
python modern_decrypt.py --password mypassword
```

## Using the Batch Files

The batch files (`encrypt.bat` and `decrypt.bat`) automatically:
- Check if Python is installed
- Install cryptography if needed
- Run the appropriate script
- Pause so you can see the results

Simply double-click the batch file or run from command prompt:
```cmd
encrypt.bat --dry-run
decrypt.bat --password mypassword
```
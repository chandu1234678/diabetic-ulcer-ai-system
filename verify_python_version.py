#!/usr/bin/env python3
"""
Quick script to verify Python version compatibility for Render deployment.
Run this locally to ensure your environment matches production.
"""

import sys
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print("=" * 60)
    print("🐍 Python Version Compatibility Check")
    print("=" * 60)
    
    print(f"\n📊 Current Python Version: {version_str}")
    print(f"   Platform: {platform.platform()}")
    print(f"   Implementation: {platform.python_implementation()}")
    
    # Check compatibility
    is_compatible = version.major == 3 and version.minor == 11
    
    if is_compatible:
        print("\n✅ COMPATIBLE: Python 3.11.x detected")
        print("   This version is compatible with all ML dependencies:")
        print("   - PyTorch 2.1.1 ✅")
        print("   - TorchVision 0.16.1 ✅")
        print("   - NumPy 1.24.3 ✅")
        print("   - Pillow 10.4.0 ✅")
        print("   - FastAPI 0.104.1 ✅")
        return True
    elif version.major == 3 and version.minor < 11:
        print(f"\n⚠️  WARNING: Python {version_str} is older than required")
        print("   Recommended: Python 3.11.9")
        print("   Some features may not work correctly")
        return False
    elif version.major == 3 and version.minor == 12:
        print(f"\n⚠️  WARNING: Python {version_str} has limited ML library support")
        print("   PyTorch 2.1.1 may not be fully compatible")
        print("   Recommended: Python 3.11.9")
        return False
    else:
        print(f"\n❌ INCOMPATIBLE: Python {version_str} is not supported")
        print("   Required: Python 3.11.x")
        print("   ML dependencies (PyTorch, TorchVision) will fail to install")
        return False

def check_render_config():
    """Check if Render configuration files exist"""
    import os
    
    print("\n" + "=" * 60)
    print("📁 Render Configuration Files")
    print("=" * 60)
    
    files_to_check = {
        "runtime.txt": "Forces Python 3.11.9 on Render",
        "render.yaml": "Render deployment configuration",
        "backend/requirements.txt": "Python dependencies",
    }
    
    all_exist = True
    for file, description in files_to_check.items():
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"\n{status} {file}")
        print(f"   {description}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_runtime_txt():
    """Verify runtime.txt content"""
    import os
    
    print("\n" + "=" * 60)
    print("🔍 runtime.txt Content")
    print("=" * 60)
    
    if not os.path.exists("runtime.txt"):
        print("\n❌ runtime.txt not found!")
        print("   Create it with: echo 'python-3.11.9' > runtime.txt")
        return False
    
    with open("runtime.txt", "r") as f:
        content = f.read().strip()
    
    print(f"\nContent: {content}")
    
    if content == "python-3.11.9":
        print("✅ Correct! Render will use Python 3.11.9")
        return True
    else:
        print(f"⚠️  Expected: python-3.11.9")
        print(f"   Found: {content}")
        return False

def main():
    print("\n🚀 Render Deployment Compatibility Check\n")
    
    # Run checks
    python_ok = check_python_version()
    config_ok = check_render_config()
    runtime_ok = check_runtime_txt()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    if python_ok and config_ok and runtime_ok:
        print("\n✅ ALL CHECKS PASSED!")
        print("   Your project is ready for Render deployment.")
        print("\n📝 Next steps:")
        print("   1. git add runtime.txt backend/requirements.txt render.yaml")
        print("   2. git commit -m 'Fix: Force Python 3.11.9 for Render'")
        print("   3. git push origin main")
        print("   4. Render will auto-deploy with Python 3.11.9")
        return 0
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("   Review the issues above before deploying.")
        
        if not python_ok:
            print("\n   Local Python version mismatch (non-critical)")
            print("   Render will use Python 3.11.9 from runtime.txt")
        
        if not config_ok:
            print("\n   Missing configuration files (critical)")
            print("   Ensure all files are created and committed")
        
        if not runtime_ok:
            print("\n   runtime.txt issue (critical)")
            print("   Fix: echo 'python-3.11.9' > runtime.txt")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())

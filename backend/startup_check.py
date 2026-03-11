#!/usr/bin/env python3
"""
Startup configuration checker for deployment verification.
Run this before deploying to catch configuration issues early.
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check critical environment variables"""
    print("🔍 Checking environment variables...")
    
    critical_vars = {
        "SECRET_KEY": "JWT signing key",
        "JWT_SECRET_KEY": "JWT token key",
    }
    
    warnings = []
    errors = []
    
    for var, description in critical_vars.items():
        value = os.getenv(var)
        if not value:
            warnings.append(f"⚠️  {var} not set ({description})")
        elif value in ["your-secret-key-change-in-production", "your-jwt-secret-key-change-in-production"]:
            errors.append(f"❌ {var} is using default value - CHANGE IN PRODUCTION!")
    
    optional_vars = {
        "DATABASE_URL": "Database connection",
        "FRONTEND_URL": "Frontend URL for CORS",
        "ALLOWED_ORIGINS": "CORS allowed origins",
    }
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if not value:
            warnings.append(f"⚠️  {var} not set ({description}) - using default")
    
    return warnings, errors

def check_model_files():
    """Check if ML model files exist"""
    print("\n🔍 Checking ML model files...")
    
    base_dir = Path(__file__).parent.parent
    model_paths = {
        "CNN Model": base_dir / "backend" / "models" / "best_dfu_model.pth",
        "Segmentation Model": base_dir / "backend" / "models" / "segmentation_model.pth",
        "Multimodal Model": base_dir / "backend" / "models" / "multimodal_model.pth",
    }
    
    warnings = []
    
    for name, path in model_paths.items():
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"  ✅ {name} found ({size_mb:.2f} MB)")
        else:
            warnings.append(f"⚠️  {name} not found at {path}")
            print(f"  ⚠️  {name} not found - will use pretrained weights")
    
    return warnings

def check_dependencies():
    """Check if critical dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    critical_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic_settings",
        "torch",
        "PIL",
    ]
    
    missing = []
    
    for package in critical_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package} not installed")
    
    return missing

def check_directory_structure():
    """Check if required directories exist"""
    print("\n🔍 Checking directory structure...")
    
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        base_dir / "backend" / "app",
        base_dir / "backend" / "models",
        base_dir / "backend" / "uploads",
    ]
    
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"  ✅ {dir_path.relative_to(base_dir)}")
        else:
            print(f"  ⚠️  {dir_path.relative_to(base_dir)} not found - will be created")
            dir_path.mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("🚀 Diabetic Ulcer AI - Startup Configuration Check")
    print("=" * 60)
    
    all_warnings = []
    all_errors = []
    
    # Check environment
    env_warnings, env_errors = check_environment()
    all_warnings.extend(env_warnings)
    all_errors.extend(env_errors)
    
    # Check models
    model_warnings = check_model_files()
    all_warnings.extend(model_warnings)
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        all_errors.append(f"❌ Missing dependencies: {', '.join(missing_deps)}")
    
    # Check directory structure
    check_directory_structure()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    if all_errors:
        print("\n❌ ERRORS (must fix before deployment):")
        for error in all_errors:
            print(f"  {error}")
    
    if all_warnings:
        print("\n⚠️  WARNINGS (non-blocking):")
        for warning in all_warnings:
            print(f"  {warning}")
    
    if not all_errors and not all_warnings:
        print("\n✅ All checks passed! Ready for deployment.")
        return 0
    elif not all_errors:
        print("\n✅ No critical errors. Warnings are non-blocking.")
        print("   Backend will start successfully with default/pretrained values.")
        return 0
    else:
        print("\n❌ Critical errors found. Fix before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

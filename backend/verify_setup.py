"""
Verification script to check all backend components are in place.
Run: python verify_setup.py
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if file exists and report."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if directory exists and report."""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def main():
    """Run full verification."""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print("\n" + "="*70)
    print("FASHION VIRTUAL TRY-ON BACKEND - VERIFICATION")
    print("="*70)
    
    all_good = True
    
    # Check core files
    print("\n📄 CORE FILES:")
    print("-" * 70)
    files_to_check = [
        ("main.py", "Main FastAPI application"),
        ("requirements.txt", "Dependencies"),
        (".env.example", "Configuration template"),
        ("README.md", "Setup documentation"),
        ("API_USAGE_GUIDE.md", "API reference"),
        ("GETTING_STARTED.md", "Quick start guide"),
        ("COMPLETION_SUMMARY.md", "Build summary"),
        ("START_HERE.md", "Index & overview"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose setup"),
        ("quickstart.py", "Setup automation"),
    ]
    
    for filename, description in files_to_check:
        if not check_file_exists(filename, description):
            all_good = False
    
    # Check directories
    print("\n📁 DIRECTORIES:")
    print("-" * 70)
    dirs_to_check = [
        ("core", "Core framework"),
        ("schemas", "Data models"),
        ("services", "Business logic"),
        ("api", "API routes"),
        ("ml_models", "ML model stubs"),
        ("scripts", "Helper scripts"),
        ("static", "Static files"),
        ("static/avatars", "Avatar uploads"),
        ("static/inputs", "Input images"),
        ("static/outputs", "Output images"),
    ]
    
    for dirname, description in dirs_to_check:
        if not check_directory_exists(dirname, description):
            all_good = False
    
    # Check key modules
    print("\n🔧 CORE MODULES:")
    print("-" * 70)
    modules = [
        ("core/__init__.py", "Core package"),
        ("core/config.py", "Configuration"),
        ("core/security.py", "JWT & RBAC"),
        ("core/db.py", "Database setup"),
        ("schemas/__init__.py", "Schemas package"),
        ("schemas/base.py", "ORM models"),
        ("schemas/models.py", "Pydantic models"),
        ("services/__init__.py", "Services package"),
        ("services/auth_service.py", "Auth service"),
        ("services/product_service.py", "Product service"),
        ("services/affiliate_service.py", "Affiliate service"),
        ("services/vton_service.py", "Try-on service"),
        ("services/pose_transfer_service.py", "Pose transfer service"),
        ("services/reco_engine.py", "Recommendation engine"),
    ]
    
    for filepath, description in modules:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check API routes
    print("\n🛣️  API ROUTES:")
    print("-" * 70)
    routes = [
        ("api/auth/__init__.py", "Auth routes"),
        ("api/products/__init__.py", "Product routes"),
        ("api/affiliate/__init__.py", "Affiliate routes"),
        ("api/tryon/__init__.py", "Try-on routes"),
        ("api/pose_transfer/__init__.py", "Pose transfer routes"),
        ("api/recommendation/__init__.py", "Recommendation routes"),
        ("api/admin/__init__.py", "Admin routes"),
    ]
    
    for filepath, description in routes:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check scripts
    print("\n⚙️  SCRIPTS:")
    print("-" * 70)
    scripts = [
        ("scripts/__init__.py", "Scripts package"),
        ("scripts/seed_data.py", "Data seeding"),
        ("scripts/test_api.py", "API testing"),
    ]
    
    for filepath, description in scripts:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check ML models
    print("\n🤖 ML MODELS (STUBS):")
    print("-" * 70)
    ml_models = [
        ("ml_models/__init__.py", "ML models package"),
        ("ml_models/hr_vton/__init__.py", "HR-VTON stub"),
        ("ml_models/pg2/__init__.py", "PG2 stub"),
        ("ml_models/openpose/__init__.py", "OpenPose stub"),
    ]
    
    for filepath, description in ml_models:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Summary
    print("\n" + "="*70)
    if all_good:
        print("✅ ALL COMPONENTS VERIFIED SUCCESSFULLY!")
        print("="*70)
        print("\n🚀 Your backend is ready to run:")
        print("\n  1. Install dependencies:")
        print("     pip install -r requirements.txt")
        print("\n  2. Start the server:")
        print("     uvicorn main:app --reload")
        print("\n  3. Open API docs:")
        print("     http://localhost:8000/docs")
        print("\n  4. Read documentation:")
        print("     - START_HERE.md (overview)")
        print("     - GETTING_STARTED.md (quick start)")
        print("     - README.md (full guide)")
        print("     - API_USAGE_GUIDE.md (all endpoints)")
        print("\n" + "="*70)
        return 0
    else:
        print("❌ SOME COMPONENTS ARE MISSING!")
        print("="*70)
        print("\nPlease check the above errors and ensure all files exist.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

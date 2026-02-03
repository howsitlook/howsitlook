"""
Quick start script to setup and run the backend.
Run: python quickstart.py
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=os.path.dirname(__file__))
        if result.returncode != 0:
            print(f"❌ Failed: {description}")
            return False
        print(f"✓ Success: {description}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run quickstart setup."""
    print("\n" + "="*60)
    print("FASHION VIRTUAL TRY-ON - Quick Start Setup")
    print("="*60)
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Determine OS and Python command
    is_windows = platform.system() == "Windows"
    python_cmd = "python" if is_windows else "python3"
    venv_activate = "venv\\Scripts\\activate" if is_windows else "source venv/bin/activate"
    
    steps = [
        (
            f"{python_cmd} -m venv venv",
            "Creating virtual environment"
        ),
        (
            f"{venv_activate} && {python_cmd} -m pip install --upgrade pip",
            "Upgrading pip"
        ),
        (
            f"{venv_activate} && {python_cmd} -m pip install -r requirements.txt",
            "Installing dependencies"
        ),
    ]
    
    # Run setup steps
    all_success = True
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            all_success = False
            break
    
    if not all_success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Create .env if doesn't exist
    env_file = os.path.join(backend_dir, ".env")
    env_example = os.path.join(backend_dir, ".env.example")
    
    print(f"\n{'='*60}")
    print("⚙️  Configuration")
    print(f"{'='*60}")
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print(f"\nℹ️  Creating .env from template...")
        with open(env_example, 'r') as f:
            env_content = f.read()
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✓ Created .env (edit with your settings)")
    
    # Seed data
    print(f"\n{'='*60}")
    print("🌱 Seeding Sample Data")
    print(f"{'='*60}")
    
    activate_cmd = f"{venv_activate} && " if is_windows else f"source {venv_activate} && "
    run_command(
        f"{activate_cmd}{python_cmd} scripts/seed_data.py",
        "Creating sample data"
    )
    
    # Final instructions
    print(f"\n{'='*60}")
    print("✓ Setup Complete!")
    print(f"{'='*60}")
    
    print(f"""
Next steps:

1. Activate virtual environment:
   {venv_activate}

2. Edit .env configuration (optional):
   - Change SECRET_KEY for production
   - Configure database URL
   - Adjust AI model settings

3. Start the server:
   uvicorn main:app --reload

4. Access API:
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health: http://localhost:8000/health

5. Test endpoints:
   python scripts/test_api.py

Sample Credentials:
   Email: admin@fashion.com
   Password: admin123456

   Email: user@fashion.com
   Password: user123456

Happy coding! 🚀
""")


if __name__ == "__main__":
    main()

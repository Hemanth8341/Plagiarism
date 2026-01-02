#!/usr/bin/env python3
"""
Plagiarism Detection System - Auto Launcher
This script automatically sets up and runs the project with a single command.
"""

import subprocess
import sys
import os
import platform
import time

def run_command(cmd, description=""):
    """Run a shell command and handle errors."""
    if description:
        print(f"\n{'='*70}")
        print(f"▶ {description}")
        print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Warning: Command completed with return code {result.returncode}")
        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    # Get the project directory (handle nested folder layout)
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    # Search upward through ancestors and perform a shallow walk to find manage.py
    def find_manage_py(start):
        cur = start
        for _ in range(8):
            # direct candidate
            candidate = os.path.join(cur, 'manage.py')
            if os.path.exists(candidate):
                return cur
            # shallow walk children (depth 2) to find manage.py in duplicated/nested folders
            try:
                for name in os.listdir(cur):
                    child = os.path.join(cur, name)
                    if os.path.isdir(child):
                        child_candidate = os.path.join(child, 'manage.py')
                        if os.path.exists(child_candidate):
                            return child
                        # check one level deeper
                        try:
                            for sub in os.listdir(child):
                                sub_child = os.path.join(child, sub)
                                if os.path.isdir(sub_child):
                                    sub_candidate = os.path.join(sub_child, 'manage.py')
                                    if os.path.exists(sub_candidate):
                                        return sub_child
                        except Exception:
                            pass
            except Exception:
                pass
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
        return None

    found = find_manage_py(workspace_root)
    if found:
        project_dir = found
    else:
        # As a fallback, try to locate within the top-level workspace folder by walking it
        repo_root = workspace_root
        # climb up looking for a folder named 'plagarism' (workspace root)
        cur = workspace_root
        while True:
            if os.path.basename(cur).lower() == 'plagarism':
                repo_root = cur
                break
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

        # search repo_root for manage.py
        project_dir = None
        for root, dirs, files in os.walk(repo_root):
            if 'manage.py' in files:
                project_dir = root
                break
        if not project_dir:
            project_dir = workspace_root

    print(f"Using project directory: {project_dir}")
    os.chdir(project_dir)
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🔍 PLAGIARISM DETECTION SYSTEM 🔍" + " "*18 + "║")
    print("║" + " "*20 + "Auto Setup & Run Launcher" + " "*24 + "║")
    print("╚" + "="*68 + "╝\n")
    
    # Step 1: Check if venv exists
    venv_path = os.path.join(project_dir, '.venv')
    if not os.path.exists(venv_path):
        print("📦 Virtual environment not found. Creating...")
        run_command(f"{sys.executable} -m venv .venv", "Step 1: Creating Virtual Environment")
    else:
        print("✅ Virtual environment already exists.\n")
    
    # Determine paths based on OS
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
        pip_exe = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        python_exe = os.path.join(venv_path, 'bin', 'python')
        pip_exe = os.path.join(venv_path, 'bin', 'pip')
    
    # Step 2: Install requirements
    print("\n📚 Installing/updating dependencies...")
    run_command(f'"{pip_exe}" install --upgrade pip', "Upgrading pip")
    run_command(f'"{pip_exe}" install -r requirements.txt', "Step 2: Installing Dependencies")
    
    # Step 3: Apply migrations
    print("\n🗄️  Applying database migrations...")
    run_command(f'"{python_exe}" manage.py migrate', "Step 3: Running Database Migrations")
    
    # Step 4: Start the server
    print("\n" + "="*70)
    print("🚀 STARTING DEVELOPMENT SERVER")
    print("="*70 + "\n")
    
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  ✅ PROJECT IS READY! Open your browser and visit:" + " "*16 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  🌐  http://127.0.0.1:8000/index.html" + " "*32 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  📌 Or navigate to:" + " "*46 + "║")
    print("║" + "     - Login: http://127.0.0.1:8000/Login.html" + " "*24 + "║")
    print("║" + "     - Register: http://127.0.0.1:8000/Register.html" + " "*18 + "║")
    print("║" + "     - Admin: http://127.0.0.1:8000/admin/" + " "*28 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  🛑 To stop the server, press CTRL+C" + " "*30 + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n\n")
    
    # Start server
    subprocess.run(f'"{python_exe}" manage.py runserver 0.0.0.0:8000', shell=True, text=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

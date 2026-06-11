#!/bin/bash
#===============================================
# Auto-Downloader Project Setup Script
#===============================================
set -e

PROJECT_DIR="/home/ubuntu/auto-downloader"
cd "$PROJECT_DIR"

echo "==> Auto-Downloader Project Setup"
echo "==> Project: $PROJECT_DIR"

#--- 1. Install system dependencies ---
echo ""
echo "==> [1/5] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y python3-pip python3-venv git curl unzip

#--- 2. Create venv and install Python deps ---
echo ""
echo "==> [2/5] Setting up Python venv..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
gallery-dl --version

#--- 3. Initialize Git ---
echo ""
echo "==> [3/5] Initializing Git..."
git init
git config user.name "Auto-Downloader Bot"
git config user.email "bot@autodownloader.local"

#---4. Install Buildozer (for local APK build test) ---
echo ""
echo "==> [4/5] Installing Buildozer..."
pip install buildozer

#--- 5. Verify project structure ---
echo ""
echo "==> [5/5] Verifying project structure..."
echo "--- Project tree:"
find . -type f | grep -v __pycache__ | grep -v ".git" | sort

echo ""
echo "============================================"
echo "✅ Project setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Edit .github/workflows/build.yml and set your GitHub repo URL"
echo "  2. git add . && git commit -m 'Initial commit'"
echo "  3. git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git"
echo "  4. git push origin main"
echo ""
echo "Or run: ./setup_project.sh --push to auto-commit and push"

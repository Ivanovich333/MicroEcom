set -e

HOOK_DIR=$(git rev-parse --git-dir)/hooks
SCRIPT_DIR=$(dirname "$0")

echo "Installing pre-commit hook..."

mkdir -p "$HOOK_DIR"

cp "$SCRIPT_DIR/pre-commit-hook.sh" "$HOOK_DIR/pre-commit"
chmod +x "$HOOK_DIR/pre-commit"

echo "Installing Python dependencies for hooks..."
pip install flake8 black isort pytest

echo "Git hooks installed successfully!"
echo "Pre-commit hook will run automatically before each commit." 
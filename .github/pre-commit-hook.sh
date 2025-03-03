set -e

echo "Running pre-commit checks..."

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -z "$STAGED_FILES" ]; then
    echo "No Python files to check. Skipping pre-commit hooks."
    exit 0
fi

SERVICES=()
for FILE in $STAGED_FILES; do
    if [[ $FILE == services/* ]]; then
        SERVICE=$(echo $FILE | cut -d'/' -f2)
        if [[ ! " ${SERVICES[@]} " =~ " ${SERVICE} " ]]; then
            SERVICES+=("$SERVICE")
        fi
    fi
done

for SERVICE in "${SERVICES[@]}"; do
    echo "Checking service: $SERVICE"
    
    cd "$(git rev-parse --show-toplevel)/services/$SERVICE"
    
    echo "Running flake8..."
    python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    echo "Running black..."
    python -m black --check .
    
    echo "Running isort..."
    python -m isort --check-only --profile black .
    
    echo "Running pytest (quick tests only)..."
    python -m pytest -m "not slow" -v
    
    echo "$SERVICE checks passed!"
done

echo "All pre-commit checks passed!"
exit 0 
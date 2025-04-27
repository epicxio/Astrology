#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies if not already installed
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:coverage_report \
    -v

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate
fi 
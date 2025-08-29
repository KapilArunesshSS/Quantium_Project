#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment
if [ -f ".env/bin/activate" ]; then
    source .env/bin/activate
else
    echo "Virtual environment not found! Make sure .env exists."
    exit 1
fi

# Run the test suite
pytest -q --disable-warnings
TEST_EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Return appropriate exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi

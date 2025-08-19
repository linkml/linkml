#!/bin/bash
# Script to run tests for LinkML monorepo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function print_usage() {
    echo "Usage: $0 [all|linkml|runtime] [options]"
    echo ""
    echo "Commands:"
    echo "  all      - Run all tests (linkml + runtime)"
    echo "  linkml   - Run only linkml tests"
    echo "  runtime  - Run only linkml_runtime tests"
    echo ""
    echo "Options:"
    echo "  --with-slow      Include slow tests"
    echo "  --with-network   Include network tests"
    echo "  --coverage       Run with coverage"
    echo ""
    echo "Examples:"
    echo "  $0 all --with-slow --with-network"
    echo "  $0 linkml --coverage"
    echo "  $0 runtime"
}

# Parse command
COMMAND=${1:-all}
shift

# Parse options
PYTEST_OPTS=""
COVERAGE_CMD=""

for arg in "$@"; do
    case $arg in
        --with-slow)
            PYTEST_OPTS="$PYTEST_OPTS --with-slow"
            ;;
        --with-network)
            PYTEST_OPTS="$PYTEST_OPTS --with-network"
            ;;
        --coverage)
            COVERAGE_CMD="coverage run -m"
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        *)
            PYTEST_OPTS="$PYTEST_OPTS $arg"
            ;;
    esac
done

# Run tests based on command
case $COMMAND in
    all)
        echo -e "${GREEN}Running all tests (linkml + runtime)...${NC}"
        uv run $COVERAGE_CMD pytest tests/ $PYTEST_OPTS
        ;;
    linkml)
        echo -e "${GREEN}Running LinkML tests only...${NC}"
        uv run $COVERAGE_CMD pytest tests/linkml/ $PYTEST_OPTS
        ;;
    runtime)
        echo -e "${GREEN}Running LinkML Runtime tests only...${NC}"
        uv run $COVERAGE_CMD pytest tests/linkml_runtime/ $PYTEST_OPTS
        ;;
    *)
        echo -e "${RED}Invalid command: $COMMAND${NC}"
        print_usage
        exit 1
        ;;
esac

# If coverage was run, show report
if [ -n "$COVERAGE_CMD" ]; then
    echo -e "${YELLOW}Generating coverage report...${NC}"
    uv run coverage xml
    uv run coverage report -m
fi
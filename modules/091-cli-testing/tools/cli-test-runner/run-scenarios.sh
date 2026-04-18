#!/usr/bin/env bash
# ============================================
# CLI Snapshot Testing — Universal Scenario Runner
# ============================================
# Inspired by Approval Tests (https://approvaltests.com/)
# by Llewellyn Falco.
#
# Reads Markdown scenario files, executes lines matching > `command`,
# inserts output as fenced code blocks, writes results back
# to the same files.
#
# Can run:
#   1. Inside Docker (default) — builds image, runs scenarios
#   2. Locally (--local) — runs directly on the host
#   3. As the inner engine (--engine) — called from within Docker
# ============================================

set -o pipefail

# ---- Defaults ----
TEST_DIR="."
PATTERN="*.md"
IMAGE_NAME="cli-snapshot-test"
NO_BUILD=false
LOCAL_MODE=false
ENGINE_MODE=false
SCENARIOS_DIR=""

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
    case "$1" in
        --test-dir|-d)    TEST_DIR="$2"; shift 2 ;;
        --pattern|-p)     PATTERN="$2"; shift 2 ;;
        --image-name|-i)  IMAGE_NAME="$2"; shift 2 ;;
        --no-build|-n)    NO_BUILD=true; shift ;;
        --local|-l)       LOCAL_MODE=true; shift ;;
        --engine|-e)      ENGINE_MODE=true; shift ;;
        --scenarios-dir)  SCENARIOS_DIR="$2"; shift 2 ;;
        *)                echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ============================================
# ENGINE MODE — processes scenario files
# This is what runs inside Docker (or locally)
# ============================================
process_scenario() {
    local FILE="$1"
    local CURRENT_DIR="/workspace"
    local TMPFILE="${FILE}.tmp"

    : > "$TMPFILE"

    local IN_OUTPUT_BLOCK=false
    local AFTER_COMMAND=false

    while IFS= read -r line || [[ -n "$line" ]]; do
        # Strip Windows CR
        line="${line//$'\r'/}"

        # Skip old output blocks (``` that follow a command)
        if $IN_OUTPUT_BLOCK; then
            if [[ "$line" == '```' ]]; then
                IN_OUTPUT_BLOCK=false
            fi
            continue
        fi

        # Detect start of old output block
        if $AFTER_COMMAND && [[ "$line" == '```' ]]; then
            IN_OUTPUT_BLOCK=true
            continue
        fi

        # Check if this line is a command: > `...`
        if [[ "$line" =~ ^\>[[:space:]]*\`(.+)\`$ ]]; then
            CMD="${BASH_REMATCH[1]}"
            AFTER_COMMAND=true

            # Write the command line
            echo "$line" >> "$TMPFILE"

            # Handle cd
            if [[ "$CMD" =~ ^cd[[:space:]]+(.*) ]]; then
                TARGET="${BASH_REMATCH[1]}"
                if [[ "$TARGET" = /* ]]; then
                    CURRENT_DIR="$TARGET"
                else
                    RESOLVED="$(cd "$CURRENT_DIR" 2>/dev/null && cd "$TARGET" 2>/dev/null && pwd)"
                    if [[ -n "$RESOLVED" ]]; then
                        CURRENT_DIR="$RESOLVED"
                    fi
                fi
                echo '```' >> "$TMPFILE"
                echo "$CURRENT_DIR" >> "$TMPFILE"
                echo '```' >> "$TMPFILE"
                continue
            fi

            # Execute command (< /dev/null prevents commands from consuming the scenario file via stdin)
            OUTPUT=$(cd "$CURRENT_DIR" 2>/dev/null && eval "$CMD" < /dev/null 2>&1) || true
            # Replace all backticks with single quotes so they don't break fenced blocks
            OUTPUT="${OUTPUT//\`/\'}"

            echo '```' >> "$TMPFILE"
            if [[ -n "$OUTPUT" ]]; then
                echo "$OUTPUT" >> "$TMPFILE"
            fi
            echo '```' >> "$TMPFILE"
        else
            AFTER_COMMAND=false
            echo "$line" >> "$TMPFILE"
        fi

    done < "$FILE"

    mv "$TMPFILE" "$FILE"
    echo "  ✓ $(basename "$FILE")"
}

if $ENGINE_MODE; then
    # Running as engine inside Docker or locally
    DIR="${SCENARIOS_DIR:-/app/scenarios}"
    echo "Running scenarios from: $DIR"
    echo "Pattern: $PATTERN"
    echo "---"

    found=0
    for f in "$DIR"/$PATTERN; do
        [ -f "$f" ] || continue
        process_scenario "$f"
        found=$((found + 1))
    done

    if [ "$found" -eq 0 ]; then
        echo "No scenario files matching '$PATTERN' found in $DIR"
        exit 1
    fi

    echo "---"
    echo "Done. $found scenario(s) processed."
    exit 0
fi

# ============================================
# LOCAL MODE — run engine directly on host
# ============================================
if $LOCAL_MODE; then
    SCENARIOS_DIR="${TEST_DIR}/scenarios"
    if [ ! -d "$SCENARIOS_DIR" ]; then
        echo "Error: scenarios directory not found: $SCENARIOS_DIR"
        exit 1
    fi

    echo "Running locally (no Docker)..."
    SCENARIOS_DIR="$SCENARIOS_DIR" ENGINE_MODE=false
    DIR="$SCENARIOS_DIR"
    echo "Running scenarios from: $DIR"
    echo "Pattern: $PATTERN"
    echo "---"

    found=0
    for f in "$DIR"/$PATTERN; do
        [ -f "$f" ] || continue
        process_scenario "$f"
        found=$((found + 1))
    done

    if [ "$found" -eq 0 ]; then
        echo "No scenario files matching '$PATTERN' found in $DIR"
        exit 1
    fi

    echo "---"
    echo "Done. $found scenario(s) processed."
    exit 0
fi

# ============================================
# DOCKER MODE — build image, mount scenarios, run
# ============================================
if [ ! -d "$TEST_DIR" ]; then
    echo "Error: test directory not found: $TEST_DIR"
    exit 1
fi

if [ ! -d "$TEST_DIR/scenarios" ]; then
    echo "Error: scenarios directory not found: $TEST_DIR/scenarios"
    exit 1
fi

if [ ! -f "$TEST_DIR/Dockerfile" ]; then
    echo "Error: Dockerfile not found: $TEST_DIR/Dockerfile"
    exit 1
fi

# Build
if ! $NO_BUILD; then
    echo "Building Docker image: $IMAGE_NAME ..."
    docker build -t "$IMAGE_NAME" -f "$TEST_DIR/Dockerfile" "$TEST_DIR"
    echo ""
fi

# Run — mount scenarios folder so output is written back to host
echo "Running scenarios in Docker..."
docker run --rm \
    -v "$(cd "$TEST_DIR/scenarios" && pwd):/app/scenarios" \
    "$IMAGE_NAME" \
    --engine --pattern "$PATTERN"

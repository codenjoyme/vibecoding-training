#!/usr/bin/env bash
# ============================================
# Skills CLI — Smoke Test Runner
# ============================================
# Reads commands.md, executes lines matching > `command`,
# inserts output as fenced code blocks, writes result
# back to the same file.
# ============================================

set -o pipefail

SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "$0")" && pwd)}"
FILE="${SCRIPT_DIR}/commands.md"

CURRENT_DIR="/workspace"
TMPFILE="${FILE}.tmp"

: > "$TMPFILE"

IN_OUTPUT_BLOCK=false
AFTER_COMMAND=false

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

        # Execute command
        OUTPUT=$(cd "$CURRENT_DIR" 2>/dev/null && eval "$CMD" 2>&1) || true
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
echo "Done. Results written to ${FILE}"

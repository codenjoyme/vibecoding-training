#!/usr/bin/env bash
set -o pipefail

SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "$0")" && pwd)}"
FILE="${SCRIPT_DIR}/commands.md"
TMPFILE="${FILE}.tmp"

: > "$TMPFILE"
IN_OUTPUT_BLOCK=false
AFTER_COMMAND=false
CURRENT_DIR="/workspace"

while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line//$'\r'/}"

    if $IN_OUTPUT_BLOCK; then
        if [[ "$line" == '```' ]]; then
            IN_OUTPUT_BLOCK=false
        fi
        continue
    fi

    if $AFTER_COMMAND && [[ "$line" == '```' ]]; then
        IN_OUTPUT_BLOCK=true
        continue
    fi

    if [[ "$line" =~ ^\>[[:space:]]*\`(.+)\`$ ]]; then
        CMD="${BASH_REMATCH[1]}"
        AFTER_COMMAND=true
        echo "$line" >> "$TMPFILE"

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

        OUTPUT="$(cd "$CURRENT_DIR" 2>/dev/null && eval "$CMD" 2>&1)" || true
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

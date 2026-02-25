#!/bin/bash
osascript << 'EOF'
tell application "Notes"
    set output to ""
    repeat with a in accounts
        set output to output & (name of a) & linefeed
    end repeat
    return output
end tell
EOF

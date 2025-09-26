#!/bin/bash

# uninstall visitor display auto-start LaunchAgent
# this script completely removes the LaunchAgent

set -e  # exit on any error

PLIST_NAME="com.visitor.display.plist"
LAUNCHAGENTS_DIR="${HOME}/Library/LaunchAgents"
PLIST_DEST="${LAUNCHAGENTS_DIR}/${PLIST_NAME}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🗑️ Uninstalling Visitor Display Auto-Start..."

# check if LaunchAgent exists
if [ ! -f "${PLIST_DEST}" ]; then
    echo "ℹ️ LaunchAgent is not installed."
    exit 0
fi

# unload the LaunchAgent if it's loaded
if launchctl list | grep -q "com.visitor.display"; then
    echo "🛑 Stopping LaunchAgent..."
    launchctl unload "${PLIST_DEST}"
    
    # wait a moment for it to fully stop
    sleep 2
    
    # verify it's stopped
    if launchctl list | grep -q "com.visitor.display"; then
        echo "⚠️ Warning: LaunchAgent may still be running. Try again or restart your Mac."
    else
        echo "✅ LaunchAgent stopped successfully."
    fi
else
    echo "ℹ️ LaunchAgent was not running."
fi

# remove the plist file
echo "🗄️ Removing plist file..."
rm -f "${PLIST_DEST}"

# clean up log files
if [ -f "${SCRIPT_DIR}/launchagent.log" ] || [ -f "${SCRIPT_DIR}/launchagent.error.log" ]; then
    echo ""
    read -p "🧹 Remove log files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "${SCRIPT_DIR}/launchagent.log"
        rm -f "${SCRIPT_DIR}/launchagent.error.log"
        echo "✅ Log files removed."
    else
        echo "ℹ️ Log files kept for your reference."
    fi
fi

echo ""
echo "✅ Visitor Display Auto-Start completely removed!"
echo ""
echo "🔄 To start the display manually, use:"
echo "   cd ${SCRIPT_DIR}"
echo "   ./display_control.sh start"
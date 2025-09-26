#!/bin/bash

# install visitor display auto-start LaunchAgent
# this script installs and loads the LaunchAgent for automatic startup

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.visitor.display.plist"
PLIST_SOURCE="${SCRIPT_DIR}/${PLIST_NAME}"
LAUNCHAGENTS_DIR="${HOME}/Library/LaunchAgents"
PLIST_DEST="${LAUNCHAGENTS_DIR}/${PLIST_NAME}"

echo "🚀 Installing Visitor Display Auto-Start..."

# create LaunchAgents directory if it doesn't exist
if [ ! -d "${LAUNCHAGENTS_DIR}" ]; then
    echo "📁 Creating LaunchAgents directory..."
    mkdir -p "${LAUNCHAGENTS_DIR}"
fi

# stop any existing service first
if launchctl list | grep -q "com.visitor.display"; then
    echo "🛑 Stopping existing service..."
    launchctl unload "${PLIST_DEST}" 2>/dev/null || true
fi

# copy plist to LaunchAgents directory
echo "📋 Installing plist file..."
cp "${PLIST_SOURCE}" "${PLIST_DEST}"

# set correct permissions
chmod 644 "${PLIST_DEST}"

# load the LaunchAgent
echo "🔄 Loading LaunchAgent..."
launchctl load "${PLIST_DEST}"

# verify it's loaded
sleep 2
if launchctl list | grep -q "com.visitor.display"; then
    echo "✅ LaunchAgent successfully installed and loaded!"
    echo ""
    echo "📊 Status:"
    launchctl list | grep com.visitor.display || echo "   Service is loading..."
    echo ""
    echo "📝 Log files will be created at:"
    echo "   Standard Output: ${SCRIPT_DIR}/launchagent.log"
    echo "   Error Output: ${SCRIPT_DIR}/launchagent.error.log"
    echo ""
    echo "🔍 To check status later, run:"
    echo "   launchctl list | grep com.visitor.display"
    echo ""
    echo "⏰ The service will start automatically after login and every 30 seconds thereafter."
else
    echo "❌ Failed to load LaunchAgent. Check the logs for details."
    exit 1
fi
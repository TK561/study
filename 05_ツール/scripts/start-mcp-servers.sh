#!/bin/bash

# Start MCP Servers for Claude Code
# This script starts Playwright MCP and Figma MCP servers on the host machine

echo "Starting MCP Servers for Claude Code..."

# Load environment variables from .env file
if [ -f "$(dirname "$0")/../.env" ]; then
    source "$(dirname "$0")/../.env"
fi

# Check if FIGMA_API_KEY is set
if [ -z "$FIGMA_API_KEY" ]; then
    echo "Error: FIGMA_API_KEY environment variable is not set."
    echo "Please set it in .env file or with: export FIGMA_API_KEY='your-api-key'"
    exit 1
fi

# Kill any existing MCP servers
echo "Stopping any existing MCP servers..."
pkill -f "playwright.*mcp" || true
pkill -f "figma-developer-mcp" || true
sleep 2

# Start Playwright MCP Server
echo "Starting Playwright MCP Server on port 9222..."
npx @playwright/mcp@latest --host 0.0.0.0 --port 9222 &
PLAYWRIGHT_PID=$!

# Wait for Playwright MCP to start
sleep 5

# Start Figma Developer MCP Server
echo "Starting Figma Developer MCP Server on port 9223..."
npx figma-developer-mcp@latest -y --figma-api-key="$FIGMA_API_KEY" --port 9223 &
FIGMA_PID=$!

# Wait for Figma MCP to start
sleep 5

echo "MCP Servers started successfully!"
echo "Playwright MCP PID: $PLAYWRIGHT_PID"
echo "Figma MCP PID: $FIGMA_PID"

# Create a PID file to track the processes
echo "$PLAYWRIGHT_PID" > /tmp/playwright-mcp.pid
echo "$FIGMA_PID" > /tmp/figma-mcp.pid

echo ""
echo "To stop the servers, run: ./scripts/stop-mcp-servers.sh"
echo ""
echo "MCP Server URLs:"
echo "  Playwright: http://localhost:9222/sse"
echo "  Figma: http://localhost:9223/sse"

# Keep the script running
wait
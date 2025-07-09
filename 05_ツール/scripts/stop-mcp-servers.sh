#!/bin/bash

# Stop MCP Servers

echo "Stopping MCP Servers..."

# Read PIDs from files if they exist
if [ -f /tmp/playwright-mcp.pid ]; then
    PLAYWRIGHT_PID=$(cat /tmp/playwright-mcp.pid)
    if kill -0 $PLAYWRIGHT_PID 2>/dev/null; then
        kill $PLAYWRIGHT_PID
        echo "Stopped Playwright MCP (PID: $PLAYWRIGHT_PID)"
    fi
    rm /tmp/playwright-mcp.pid
fi

if [ -f /tmp/figma-mcp.pid ]; then
    FIGMA_PID=$(cat /tmp/figma-mcp.pid)
    if kill -0 $FIGMA_PID 2>/dev/null; then
        kill $FIGMA_PID
        echo "Stopped Figma MCP (PID: $FIGMA_PID)"
    fi
    rm /tmp/figma-mcp.pid
fi

# Also kill by process name as backup
pkill -f "playwright.*mcp" || true
pkill -f "figma-developer-mcp" || true

echo "MCP Servers stopped."
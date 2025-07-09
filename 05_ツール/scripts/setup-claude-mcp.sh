#!/bin/bash

# Setup Claude Code with MCP Servers in devcontainer
# Run this script inside the devcontainer after authentication

echo "Setting up Claude Code with MCP Servers..."

# Add Playwright MCP
echo "Adding Playwright MCP..."
claude mcp add --transport sse playwright http://host.docker.internal:9222/sse -s project

# Add Figma Developer MCP
echo "Adding Figma Developer MCP..."
claude mcp add --transport sse figma http://host.docker.internal:9223/sse -s project

# List registered MCPs
echo ""
echo "Registered MCP Servers:"
claude mcp list

echo ""
echo "Setup complete! You can now use Claude Code with Playwright and Figma MCP."
echo ""
echo "Example commands:"
echo "  - 'Playwright MCPでGoogleを開いて'"
echo "  - 'Figmaのデザインファイル[URL]を確認して'"
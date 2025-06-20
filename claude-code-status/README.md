# Claude Code Status

VS Code extension to display Claude Code usage and plan status in the status bar.

## Features

- Display current Claude Code plan (Claude Max or Usage-based)
- Show usage statistics for usage-based plans
- Visual indicators for usage levels (warning at 75%, error at 90%)
- Refresh status manually or automatically
- Quick access to detailed information

## Requirements

- Claude Code CLI must be installed and available in PATH
- VS Code 1.74.0 or higher

## Extension Settings

This extension contributes the following settings:

* `claudeCodeStatus.refreshInterval`: How often to refresh status in seconds (default: 300)
* `claudeCodeStatus.showInStatusBar`: Show Claude Code status in status bar (default: true)

## Commands

* `Claude Code: Refresh Status` - Manually refresh the current status
* `Claude Code: Show Details` - Show detailed status information

## Installation

1. Clone this repository
2. Run `npm install`
3. Run `npm run compile`
4. Press F5 to open a new VS Code window with the extension loaded

## Building

To create a VSIX package:

```bash
npm run compile
npx vsce package
```
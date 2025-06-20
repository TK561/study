import * as vscode from 'vscode';
import { ClaudeCodeStatusProvider } from './statusProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('Claude Code Status extension is now active!');

    const statusProvider = new ClaudeCodeStatusProvider(context);

    const refreshCommand = vscode.commands.registerCommand('claude-code-status.refresh', () => {
        statusProvider.refresh();
        vscode.window.showInformationMessage('Claude Code status refreshed!');
    });

    const showDetailsCommand = vscode.commands.registerCommand('claude-code-status.showDetails', () => {
        statusProvider.showDetails();
    });

    context.subscriptions.push(refreshCommand);
    context.subscriptions.push(showDetailsCommand);
    context.subscriptions.push(statusProvider);

    statusProvider.start();
}

export function deactivate() {}
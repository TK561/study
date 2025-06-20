import * as vscode from 'vscode';
import { ClaudeCodeAPI, ClaudeCodeStatus } from './claudeCodeApi';

export class ClaudeCodeStatusProvider {
    private statusBarItem: vscode.StatusBarItem;
    private api: ClaudeCodeAPI;
    private refreshTimer?: NodeJS.Timeout;
    private currentStatus?: ClaudeCodeStatus;

    constructor(private context: vscode.ExtensionContext) {
        this.api = new ClaudeCodeAPI();
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this.statusBarItem.command = 'claude-code-status.showDetails';
    }

    async start() {
        const config = vscode.workspace.getConfiguration('claudeCodeStatus');
        const showInStatusBar = config.get<boolean>('showInStatusBar', true);
        
        if (showInStatusBar) {
            this.statusBarItem.show();
            await this.refresh();
            
            const refreshInterval = config.get<number>('refreshInterval', 300) * 1000;
            this.refreshTimer = setInterval(() => {
                this.refresh();
            }, refreshInterval);
        }
    }

    async refresh() {
        this.statusBarItem.text = '$(sync~spin) Claude Code...';
        
        try {
            this.currentStatus = await this.api.getStatus();
            this.updateStatusBar();
        } catch (error) {
            this.statusBarItem.text = '$(error) Claude Code Error';
            this.statusBarItem.tooltip = error instanceof Error ? error.message : 'Unknown error';
        }
    }

    private updateStatusBar() {
        if (!this.currentStatus) {
            return;
        }

        if (this.currentStatus.plan === 'Claude Max') {
            this.statusBarItem.text = '$(check) Claude Max';
            this.statusBarItem.tooltip = 'Claude Max subscription - Unlimited usage';
            this.statusBarItem.backgroundColor = undefined;
        } else if (this.currentStatus.plan === 'Claude Pro') {
            this.statusBarItem.text = '$(star) Claude Pro';
            this.statusBarItem.tooltip = 'Claude Pro subscription - Enhanced features';
            this.statusBarItem.backgroundColor = undefined;
        } else if (this.currentStatus.plan === 'Usage-based' && this.currentStatus.usage) {
            const { current, limit, percentage } = this.currentStatus.usage;
            this.statusBarItem.text = `$(graph) Claude: $${current.toFixed(2)}/$${limit.toFixed(2)}`;
            this.statusBarItem.tooltip = `Usage: ${percentage.toFixed(1)}%\nCurrent: $${current.toFixed(2)}\nLimit: $${limit.toFixed(2)}`;
            
            if (percentage >= 90) {
                this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
            } else if (percentage >= 75) {
                this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            } else {
                this.statusBarItem.backgroundColor = undefined;
            }
        } else if (this.currentStatus.plan === 'Token-based') {
            this.statusBarItem.text = '$(info) Claude: Token-based';
            this.statusBarItem.tooltip = 'Token-based usage - Click for details';
            this.statusBarItem.backgroundColor = undefined;
        } else if (this.currentStatus.plan === 'Available') {
            this.statusBarItem.text = '$(info) Claude: Available';
            this.statusBarItem.tooltip = 'Claude Code is available - Click for cost info';
            this.statusBarItem.backgroundColor = undefined;
        } else if (this.currentStatus.plan === 'Info unavailable') {
            this.statusBarItem.text = '$(question) Claude: No data';
            this.statusBarItem.tooltip = 'Cost information not available';
            this.statusBarItem.backgroundColor = undefined;
        } else if (this.currentStatus.plan === 'Not installed') {
            this.statusBarItem.text = '$(error) Claude: Not found';
            this.statusBarItem.tooltip = 'Claude Code CLI not installed';
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        } else if (this.currentStatus.error) {
            this.statusBarItem.text = `$(warning) Claude: ${this.currentStatus.plan}`;
            this.statusBarItem.tooltip = this.currentStatus.error;
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        }
    }

    async showDetails() {
        if (!this.currentStatus) {
            await this.refresh();
        }

        if (!this.currentStatus) {
            vscode.window.showErrorMessage('Could not retrieve Claude Code status');
            return;
        }

        const items: vscode.QuickPickItem[] = [];

        if (this.currentStatus.plan === 'Claude Max') {
            items.push({
                label: '$(check) Claude Max Subscription',
                description: 'Unlimited usage included'
            });
        } else if (this.currentStatus.plan === 'Claude Pro') {
            items.push({
                label: '$(star) Claude Pro Subscription',
                description: 'Enhanced features and priority access'
            });
        } else if (this.currentStatus.plan === 'Usage-based' && this.currentStatus.usage) {
            const { current, limit, percentage } = this.currentStatus.usage;
            items.push({
                label: '$(graph) Usage-based Plan',
                description: `$${current.toFixed(2)} / $${limit.toFixed(2)} (${percentage.toFixed(1)}%)`
            });
            
            const remaining = limit - current;
            items.push({
                label: '$(info) Remaining Budget',
                description: `$${remaining.toFixed(2)}`
            });
        } else if (this.currentStatus.plan === 'Token-based') {
            items.push({
                label: '$(info) Token-based Usage',
                description: 'Check Claude Code dashboard for usage details'
            });
        } else if (this.currentStatus.plan === 'Available') {
            items.push({
                label: '$(info) Claude Code Available',
                description: 'Cost information available online'
            });
        } else if (this.currentStatus.plan === 'Info unavailable') {
            items.push({
                label: '$(question) Information Unavailable',
                description: 'Cost data could not be retrieved'
            });
        } else if (this.currentStatus.plan === 'Not installed') {
            items.push({
                label: '$(error) Claude Code CLI Not Found',
                description: 'Please install Claude Code CLI'
            });
        } else if (this.currentStatus.error) {
            items.push({
                label: `$(warning) ${this.currentStatus.plan}`,
                description: this.currentStatus.error
            });
        }

        items.push({
            label: '$(refresh) Refresh Status',
            description: 'Update the current status'
        });

        const selection = await vscode.window.showQuickPick(items, {
            placeHolder: 'Claude Code Status Details'
        });

        if (selection?.label === '$(refresh) Refresh Status') {
            await this.refresh();
        }
    }

    dispose() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        this.statusBarItem.dispose();
    }
}
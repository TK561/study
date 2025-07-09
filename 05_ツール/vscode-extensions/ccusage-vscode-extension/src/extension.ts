import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface UsageData {
    model: string;
    tokens: number;
    cost: number;
    dailyCost: number;
    timeRemaining?: string;
    sessionProgress?: number;
    projectedTokens?: number;
    projectedCost?: number;
    burnRate?: number;
    isPro?: boolean;
    isMax?: boolean;
    isActive?: boolean;
    sessionStart?: string;
    sessionEnd?: string;
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Claude Code Status is now active!');

    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );

    statusBarItem.command = 'claudeCodeStatus.showDetails';
    statusBarItem.show();

    let updateInterval: NodeJS.Timer | undefined;

    const updateStatusBar = async () => {
        const config = vscode.workspace.getConfiguration('claudeCodeStatus');
        const enabled = config.get<boolean>('enabled', true);
        
        if (!enabled) {
            statusBarItem.hide();
            return;
        }

        statusBarItem.show();
        statusBarItem.text = '$(sync~spin) Fetching usage...';

        try {
            const command = config.get<string>('command', 'npx ccusage@latest blocks');
            const { stdout } = await execAsync(command, {
                shell: process.platform === 'win32' ? 'cmd.exe' : '/bin/bash',
                timeout: 10000
            });
            
            const usageData = parseUsageData(stdout);
            
            if (usageData) {
                const showCurrency = config.get<string>('showCurrency', 'USD');
                const jpyRate = config.get<number>('jpyRate', 150);
                const showTimeRemaining = config.get<boolean>('showTimeRemaining', true);
                
                let statusText = '';
                
                // Plan indicator
                if (usageData.isMax) {
                    statusText = '$(zap) MAX ';
                } else if (usageData.isPro) {
                    statusText = '$(star) Pro ';
                } else {
                    statusText = '$(cloud) ';
                }
                
                // Model
                statusText += `${usageData.model} `;
                
                // Tokens
                statusText += `$(arrow-right) ${formatTokens(usageData.tokens)} `;
                
                // Cost
                if (showCurrency === 'JPY') {
                    const jpyCost = usageData.cost * jpyRate;
                    statusText += `$(credit-card) ¥${jpyCost.toFixed(0)} `;
                } else {
                    statusText += `$(credit-card) $${usageData.cost.toFixed(2)} `;
                }
                
                // Session progress
                if (usageData.sessionProgress) {
                    statusText += `$(clock) ${usageData.sessionProgress.toFixed(1)}% `;
                }
                
                // Time remaining
                if (showTimeRemaining && usageData.timeRemaining) {
                    statusText += `$(watch) ${usageData.timeRemaining}`;
                }
                
                // Active indicator
                if (usageData.isActive) {
                    statusText += ' $(pulse)';
                }
                
                statusBarItem.text = statusText;
                statusBarItem.tooltip = createTooltip(usageData, showCurrency, jpyRate);
                
                // Update background color based on burn rate
                if (usageData.burnRate) {
                    if (usageData.burnRate > 50000) {
                        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
                    } else if (usageData.burnRate > 30000) {
                        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
                    } else {
                        statusBarItem.backgroundColor = undefined;
                    }
                }
                
            } else {
                statusBarItem.text = '$(warning) Failed to parse usage data';
                statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
            }
        } catch (error) {
            console.error('Error fetching usage:', error);
            statusBarItem.text = '$(error) Error fetching usage';
            statusBarItem.tooltip = `Error: ${error}`;
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        }
    };

    const startUpdateInterval = () => {
        const config = vscode.workspace.getConfiguration('claudeCodeStatus');
        const interval = config.get<number>('interval', 5000); // 5秒間隔に短縮
        
        if (updateInterval) {
            clearInterval(updateInterval);
        }
        
        updateInterval = setInterval(updateStatusBar, interval);
    };

    // Initial update
    updateStatusBar();
    startUpdateInterval();

    // Register commands
    const refreshCommand = vscode.commands.registerCommand('claudeCodeStatus.refresh', () => {
        updateStatusBar();
    });

    const showDetailsCommand = vscode.commands.registerCommand('claudeCodeStatus.showDetails', async () => {
        const terminal = vscode.window.createTerminal('Claude Code Usage');
        terminal.sendText('npx ccusage@latest blocks --live');
        terminal.show();
    });

    const showConfigCommand = vscode.commands.registerCommand('claudeCodeStatus.showConfig', () => {
        vscode.commands.executeCommand('workbench.action.openSettings', 'claudeCodeStatus');
    });

    // Watch for configuration changes
    const configWatcher = vscode.workspace.onDidChangeConfiguration((e) => {
        if (e.affectsConfiguration('claudeCodeStatus')) {
            updateStatusBar();
            startUpdateInterval();
        }
    });

    context.subscriptions.push(
        statusBarItem,
        refreshCommand,
        showDetailsCommand,
        showConfigCommand,
        configWatcher
    );

    if (updateInterval) {
        context.subscriptions.push({
            dispose: () => clearInterval(updateInterval)
        });
    }
}

function parseUsageData(output: string): UsageData | null {
    try {
        // Check if this is an error output
        if (output.includes('Error:') || output.includes('No valid Claude data directories found')) {
            return null;
        }
        
        // Parse session start time from blocks format: "7/9/2025, 1:00:00 AM"
        let sessionStart: string | undefined;
        const sessionStartMatch = output.match(/(\d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2}:\d{2} [AP]M)/);
        if (sessionStartMatch) {
            const fullUtcTime = sessionStartMatch[1];
            const timeOnly = fullUtcTime.split(', ')[1]; // Extract "1:00:00 AM"
            sessionStart = convertToJST(timeOnly);
            console.log(`[Claude Code Status] Session Start - UTC: ${timeOnly}, JST: ${sessionStart}`);
        }
        
        // Parse remaining time and calculate session end
        let sessionEnd: string | undefined;
        const remainingMatch = output.match(/(\d+h \d+m|\d+h|\d+m) remaining/);
        if (remainingMatch && sessionStart) {
            const remainingTime = remainingMatch[1];
            sessionEnd = calculateSessionEnd(sessionStart, remainingTime);
            console.log(`[Claude Code Status] Session End calculated - JST: ${sessionEnd}`);
        }
        
        // Parse session progress
        let sessionProgress = 0;
        const progressMatch = output.match(/(\d+\.?\d*)%/);
        if (progressMatch) {
            sessionProgress = parseFloat(progressMatch[1]);
        }
        
        // Parse time remaining from live view format: "Remaining: 2h (06:00:00 AM)"
        let timeRemaining: string | undefined;
        const timeRemainingMatch = output.match(/Remaining: (\d+h(?: \d+m)?)/);
        if (timeRemainingMatch) {
            timeRemaining = timeRemainingMatch[1];
        } else {
            // Fallback to other patterns
            const altTimeMatch = output.match(/(\d+h \d+m|\d+h|\d+m)/);
            if (altTimeMatch) {
                timeRemaining = altTimeMatch[1];
            }
        }
        
        // Parse tokens - look for current usage from live view
        let tokens = 0;
        // First try to get from live view format: "Tokens: 52,252 (Burn Rate: ...)"
        const liveTokensMatch = output.match(/Tokens: ([\d,]+) \(Burn Rate:/);
        if (liveTokensMatch) {
            tokens = parseInt(liveTokensMatch[1].replace(/,/g, ''));
        } else {
            // Fallback to other patterns
            const tokensMatch = output.match(/Tokens: ([\d,]+)/);
            if (tokensMatch) {
                tokens = parseInt(tokensMatch[1].replace(/,/g, ''));
            } else {
                // Alternative pattern for live view with k/m/b suffix
                const liveTokensKMBMatch = output.match(/\((\d+\.?\d*[kmb]?) tokens\)/i);
                if (liveTokensKMBMatch) {
                    const tokenStr = liveTokensKMBMatch[1].toLowerCase();
                    if (tokenStr.includes('k')) {
                        tokens = parseFloat(tokenStr) * 1000;
                    } else if (tokenStr.includes('m')) {
                        tokens = parseFloat(tokenStr) * 1000000;
                    } else if (tokenStr.includes('b')) {
                        tokens = parseFloat(tokenStr) * 1000000000;
                    } else {
                        tokens = parseFloat(tokenStr);
                    }
                }
            }
        }
        
        // Parse cost from live view format
        let cost = 0;
        // Look for cost in the usage section: "Cost: $3.87"
        const costMatch = output.match(/Cost: \$?([\d.]+)/);
        if (costMatch) {
            cost = parseFloat(costMatch[1]);
        }
        
        // Parse projected tokens and cost
        let projectedTokens = 0;
        let projectedCost = 0;
        const projectedTokensMatch = output.match(/Tokens: ([\d,]+\.\d*[kmb]?)/);
        if (projectedTokensMatch) {
            const tokenStr = projectedTokensMatch[1].toLowerCase();
            if (tokenStr.includes('k')) {
                projectedTokens = parseFloat(tokenStr) * 1000;
            } else if (tokenStr.includes('m')) {
                projectedTokens = parseFloat(tokenStr) * 1000000;
            } else if (tokenStr.includes('b')) {
                projectedTokens = parseFloat(tokenStr) * 1000000000;
            } else {
                projectedTokens = parseFloat(tokenStr.replace(/,/g, ''));
            }
        }
        
        const projectedCostMatch = output.match(/Cost: \$?([\d.]+)/g);
        if (projectedCostMatch && projectedCostMatch.length > 1) {
            projectedCost = parseFloat(projectedCostMatch[1].replace('$', ''));
        }
        
        // Parse burn rate
        let burnRate = 0;
        const burnRateMatch = output.match(/Burn Rate: ([\d,]+) token\/min/);
        if (burnRateMatch) {
            burnRate = parseInt(burnRateMatch[1].replace(/,/g, ''));
        }
        
        // Parse models from live view format: "⚙️  Models: opus-4, sonnet-4"
        let model = 'unknown';
        const modelMatch = output.match(/⚙️\s+Models: (.+)/);
        if (modelMatch) {
            model = modelMatch[1].trim();
        } else {
            // Fallback to other patterns
            const altModelMatch = output.match(/Models: (.+)/);
            if (altModelMatch) {
                model = altModelMatch[1].trim();
            } else {
                // Try to find model in other patterns
                if (output.includes('opus-4')) {
                    model = 'opus-4';
                } else if (output.includes('sonnet-4')) {
                    model = 'sonnet-4';
                } else if (output.includes('haiku-4')) {
                    model = 'haiku-4';
                }
            }
        }
        
        // Check for Pro/MAX status - ccusage doesn't explicitly show plan type in output
        // Check for session characteristics instead
        const hasSessionLimit = output.includes('remaining') || output.includes('Remaining');
        const hasOpusModel = output.includes('opus-4');
        
        // If using opus-4 and has session time limits, likely MAX plan
        // If has session limits but no opus-4, likely Pro plan
        const isMax = hasOpusModel && hasSessionLimit;
        const isPro = hasSessionLimit && !hasOpusModel;
        
        // Check if session is active
        const isActive = output.includes('ACTIVE') || output.includes('LIVE');
        
        return {
            model,
            tokens,
            cost,
            dailyCost: cost, // For now, use same as cost
            timeRemaining,
            sessionProgress,
            projectedTokens,
            projectedCost,
            burnRate,
            isPro,
            isMax,
            isActive,
            sessionStart,
            sessionEnd
        };
    } catch (error) {
        console.error('Error parsing usage data:', error);
        return null;
    }
}

function formatTokens(tokens: number): string {
    if (tokens >= 1000000000) {
        return `${(tokens / 1000000000).toFixed(1)}B`;
    } else if (tokens >= 1000000) {
        return `${(tokens / 1000000).toFixed(1)}M`;
    } else if (tokens >= 1000) {
        return `${(tokens / 1000).toFixed(1)}K`;
    }
    return tokens.toString();
}

function createTooltip(data: UsageData, currency: string, jpyRate: number): string {
    let tooltip = `Claude Code Usage Stats\n`;
    tooltip += `─────────────────────────\n`;
    tooltip += `Model: ${data.model}\n`;
    tooltip += `Tokens: ${formatTokens(data.tokens)}\n`;
    
    if (currency === 'JPY') {
        tooltip += `Cost: ¥${(data.cost * jpyRate).toFixed(0)}\n`;
        tooltip += `(Rate: $1 = ¥${jpyRate})\n`;
    } else {
        tooltip += `Cost: $${data.cost.toFixed(2)}\n`;
    }
    
    if (data.sessionStart) {
        tooltip += `Session Start: ${data.sessionStart}\n`;
    }
    
    if (data.sessionEnd) {
        tooltip += `Session End: ${data.sessionEnd}\n`;
    }
    
    if (data.sessionProgress) {
        tooltip += `Session Progress: ${data.sessionProgress.toFixed(1)}%\n`;
    }
    
    if (data.timeRemaining) {
        tooltip += `Time Remaining: ${data.timeRemaining}\n`;
    }
    
    if (data.burnRate) {
        tooltip += `Burn Rate: ${data.burnRate.toLocaleString()} tokens/min\n`;
    }
    
    if (data.projectedTokens) {
        tooltip += `Projected Tokens: ${formatTokens(data.projectedTokens)}\n`;
    }
    
    if (data.projectedCost) {
        if (currency === 'JPY') {
            tooltip += `Projected Cost: ¥${(data.projectedCost * jpyRate).toFixed(0)}\n`;
        } else {
            tooltip += `Projected Cost: $${data.projectedCost.toFixed(2)}\n`;
        }
    }
    
    tooltip += `─────────────────────────\n`;
    
    if (data.isPro) {
        tooltip += `Plan: Pro\n`;
    } else if (data.isMax) {
        tooltip += `Plan: MAX\n`;
    }
    
    if (data.isActive) {
        tooltip += `Status: Active Session\n`;
    }
    
    tooltip += `\nClick to open live view`;
    tooltip += `\nRight-click → Refresh to update`;
    
    return tooltip;
}

function convertToJST(utcTimeString: string): string {
    try {
        // Parse UTC time string like "01:00:00 AM" 
        const today = new Date();
        const [time, ampm] = utcTimeString.split(' ');
        const [hours, minutes, seconds] = time.split(':').map(Number);
        
        // Convert to 24-hour format
        let hour24 = hours;
        if (ampm === 'PM' && hours !== 12) {
            hour24 += 12;
        } else if (ampm === 'AM' && hours === 12) {
            hour24 = 0;
        }
        
        // Create UTC date
        const utcDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), hour24, minutes, seconds);
        
        // Convert to JST (UTC+9)
        const jstDate = new Date(utcDate.getTime() + (9 * 60 * 60 * 1000));
        
        // Format as Japanese time
        const jstHour = jstDate.getHours();
        const jstMinute = jstDate.getMinutes();
        const jstSecond = jstDate.getSeconds();
        
        const jstHour12 = jstHour === 0 ? 12 : jstHour > 12 ? jstHour - 12 : jstHour;
        const jstAmPm = jstHour < 12 ? 'AM' : 'PM';
        
        return `${jstHour12.toString().padStart(2, '0')}:${jstMinute.toString().padStart(2, '0')}:${jstSecond.toString().padStart(2, '0')} ${jstAmPm}`;
    } catch (error) {
        // If conversion fails, return original string
        return utcTimeString;
    }
}

function calculateSessionEnd(startTimeJST: string, remainingTime: string): string {
    try {
        // Parse start time
        const [time, ampm] = startTimeJST.split(' ');
        const [hours, minutes, seconds] = time.split(':').map(Number);
        
        let hour24 = hours;
        if (ampm === 'PM' && hours !== 12) {
            hour24 += 12;
        } else if (ampm === 'AM' && hours === 12) {
            hour24 = 0;
        }
        
        // Create start date
        const today = new Date();
        const startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), hour24, minutes, seconds);
        
        // Parse remaining time
        const hoursMatch = remainingTime.match(/(\d+)h/);
        const minutesMatch = remainingTime.match(/(\d+)m/);
        
        const remainingHours = hoursMatch ? parseInt(hoursMatch[1]) : 0;
        const remainingMinutes = minutesMatch ? parseInt(minutesMatch[1]) : 0;
        
        // Calculate end time
        const endDate = new Date(startDate.getTime() + (remainingHours * 60 * 60 * 1000) + (remainingMinutes * 60 * 1000));
        
        // Format as 12-hour time
        const endHour = endDate.getHours();
        const endMinute = endDate.getMinutes();
        const endSecond = endDate.getSeconds();
        
        const endHour12 = endHour === 0 ? 12 : endHour > 12 ? endHour - 12 : endHour;
        const endAmPm = endHour < 12 ? 'AM' : 'PM';
        
        return `${endHour12.toString().padStart(2, '0')}:${endMinute.toString().padStart(2, '0')}:${endSecond.toString().padStart(2, '0')} ${endAmPm}`;
    } catch (error) {
        return 'Unknown';
    }
}

export function deactivate() {}
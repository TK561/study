import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface ClaudeCodeStatus {
    plan: string;
    usage?: {
        current: number;
        limit: number;
        percentage: number;
    };
    error?: string;
}

export class ClaudeCodeAPI {
    async getStatus(): Promise<ClaudeCodeStatus> {
        try {
            const { stdout } = await execAsync('claude cost', { encoding: 'utf8' });
            
            // Check for Claude Max subscription
            if (stdout.includes('Claude Max subscription') || stdout.includes('your subscription includes Claude Code usage')) {
                return {
                    plan: 'Claude Max',
                    usage: undefined
                };
            }
            
            // Check for Claude Pro subscription
            if (stdout.includes('Claude Pro') || stdout.includes('Pro subscription') || stdout.includes('Pro plan')) {
                return {
                    plan: 'Claude Pro',
                    usage: undefined
                };
            }
            
            // Check for token-based pricing message
            if (stdout.includes('token-based pricing') && stdout.includes('console.anthropic.com')) {
                return {
                    plan: 'Token-based',
                    usage: undefined
                };
            }
            
            // Check for usage-based billing patterns
            const dollarUsageMatch = stdout.match(/\$(\d+(?:\.\d+)?)\s*\/\s*\$(\d+(?:\.\d+)?)/);
            if (dollarUsageMatch) {
                const current = parseFloat(dollarUsageMatch[1]);
                const limit = parseFloat(dollarUsageMatch[2]);
                const percentage = (current / limit) * 100;
                
                return {
                    plan: 'Usage-based',
                    usage: {
                        current,
                        limit,
                        percentage
                    }
                };
            }
            
            // Check for token-based usage patterns
            const tokenMatch = stdout.match(/(\d+(?:,\d+)*)\s*(?:tokens?\s*)?(?:used|consumed|processed)/i);
            if (tokenMatch) {
                return {
                    plan: 'Token-based',
                    error: 'Token usage detected - check Claude Code dashboard for details'
                };
            }
            
            // If output contains cost/pricing information but no specific usage
            if (stdout.includes('cost') || stdout.includes('pricing') || stdout.includes('token')) {
                return {
                    plan: 'Available',
                    error: 'Cost information available - check https://docs.anthropic.com/en/docs/claude-code/costs'
                };
            }
            
            // If no cost information found
            return {
                plan: 'Info unavailable',
                error: 'Cost command returned no usage data'
            };
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            
            if (errorMessage.includes('command not found') || errorMessage.includes('claude: not found')) {
                return {
                    plan: 'Not installed',
                    error: 'Claude Code CLI not found'
                };
            }
            
            if (errorMessage.includes('permission') || errorMessage.includes('access')) {
                return {
                    plan: 'Access error',
                    error: 'Permission or access issue with Claude CLI'
                };
            }
            
            return {
                plan: 'Error',
                error: errorMessage
            };
        }
    }
}
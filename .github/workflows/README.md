# GitHub Actions CI/CD Pipeline

## Overview
Complete automation system for Vercel deployment with Claude Code integration.

## Workflows

### 1. `vercel-deploy.yml`
**Trigger**: Push to main branch
**Purpose**: Deploy to Vercel with error handling

**Flow**:
1. Deploy to Vercel
2. Test deployment health
3. Create GitHub Issue on failure
4. Trigger Claude Code auto-fix

### 2. `claude-autofix.yml` 
**Trigger**: Manual dispatch or auto-triggered on failures
**Purpose**: Automatic error resolution using Claude Code

**Capabilities**:
- Analyze common Vercel deployment issues
- Apply standardized fixes
- Test fixes automatically
- Update GitHub Issues with results

### 3. `monitoring.yml`
**Trigger**: Scheduled (every 30 minutes)
**Purpose**: Continuous health monitoring

**Checks**:
- Main page availability (200 status)
- API endpoint health
- Response time monitoring
- Auto-alert on failures

## Required Secrets

Add these to your GitHub repository secrets:

```
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id  
VERCEL_PROJECT_ID=prj_gm8o7yYpKf4fEf1ydU5oQwZGH5dV
GITHUB_TOKEN=automatic (provided by GitHub)
```

## Auto-Fix Features

### Common Issues Resolved:
-  Vercel configuration errors
-  Python function format issues  
-  Runtime specification problems
-  Simple syntax errors
-  Dependencies conflicts

### Manual Review Required:
- Complex logic errors
- Security vulnerabilities
- Performance issues
- API integration problems

## Usage

### Trigger Auto-Fix Manually:
```bash
# Via GitHub CLI
gh workflow run claude-autofix.yml \
  -f error_type=deployment_failure \
  -f deployment_url=https://your-deployment.vercel.app

# Via GitHub UI
Actions > Claude Code Auto-Fix > Run workflow
```

### Monitor Deployment:
- Check Actions tab for workflow status
- Issues tab for automated error reports
- Vercel dashboard for deployment details

## Integration Benefits

1. **Zero-downtime goal**: Automatic error detection and resolution
2. **Faster feedback**: Issues created immediately on failures  
3. **Learning system**: Patterns recognized and fixed automatically
4. **Audit trail**: All fixes documented in GitHub Issues
5. **24/7 monitoring**: Continuous health checks

## Emergency Procedures

If auto-fix fails:
1. Check workflow logs in Actions tab
2. Review created GitHub Issue for details
3. Manual investigation may be required
4. Contact system administrator if needed

---
 **Powered by Claude Code GitHub Actions Integration**
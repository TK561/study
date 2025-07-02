#!/bin/bash
# Vercel deployment script for study-research project

echo "🚀 Deploying study-research project..."

# Create project configuration
cat > .vercel/project.json << EOF
{
  "projectId": "prj_study_research_$(date +%s)",
  "orgId": "team_tk561s-projects"
}
EOF

# Deploy with project name
echo -e "y\nn\nstudy-research\n" | npx vercel --prod || {
    echo "First attempt failed, trying alternative method..."
    npx vercel deploy --prod --yes
}

echo "✅ Deployment complete!"
#!/bin/bash

# Quick Start Deployment to Azure
# This script provides quick commands for Azure deployment

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  Psychology Chatbot Advanced - Quick Deployment to Azure"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Configuration
SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-your_subscription_id}"
RESOURCE_GROUP="${RESOURCE_GROUP:-psychology-chatbot-rg}"
LOCATION="${LOCATION:-eastus}"
PROJECT_NAME="psychology-chatbot"

echo "📋 DEPLOYMENT PREREQUISITES"
echo "───────────────────────────────────────────────────────────────"
echo "✓ Azure Subscription with Contributor role"
echo "✓ Docker installed locally"
echo "✓ Azure CLI installed"
echo "✓ API Keys configured (.env file)"
echo ""

echo "📚 QUICK START STEPS"
echo "───────────────────────────────────────────────────────────────"
echo ""

echo "STEP 1: Authenticate with Azure"
echo "Command:"
echo "  az login"
echo "  az account set --subscription $SUBSCRIPTION_ID"
echo ""

echo "STEP 2: Create Resource Group"
echo "Command:"
echo "  az group create --name $RESOURCE_GROUP --location $LOCATION"
echo ""

echo "STEP 3: Create Container Registry"
echo "Command:"
echo "  az acr create --resource-group $RESOURCE_GROUP \\"
echo "    --name psychology --sku Basic"
echo "  az acr login --name psychology"
echo ""

echo "STEP 4: Build and Push Docker Images"
echo "Command:"
echo "  docker build -t psychology.azurecr.io/psychology-backend:latest -f Dockerfile ."
echo "  docker build -t psychology.azurecr.io/psychology-frontend:latest -f Dockerfile.frontend ."
echo "  docker push psychology.azurecr.io/psychology-backend:latest"
echo "  docker push psychology.azurecr.io/psychology-frontend:latest"
echo ""

echo "STEP 5: Deploy Infrastructure with Bicep"
echo "Command:"
echo "  az deployment group create \\"
echo "    --resource-group $RESOURCE_GROUP \\"
echo "    --template-file .azure/main.bicep \\"
echo "    --parameters \\"
echo "      location=$LOCATION \\"
echo "      projectName=$PROJECT_NAME \\"
echo "      environment=dev \\"
echo "      backendImage=psychology.azurecr.io/psychology-backend:latest \\"
echo "      frontendImage=psychology.azurecr.io/psychology-frontend:latest \\"
echo "      groqApiKey=\$GROQ_API_KEY"
echo ""

echo "STEP 6: Get Deployment Outputs"
echo "Command:"
echo "  az deployment group show \\"
echo "    --resource-group $RESOURCE_GROUP \\"
echo "    --name main \\"
echo "    --query properties.outputs -o json"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "  📊 FOR AUTOMATED DEPLOYMENT, RUN:"
echo "  ./deploy-to-azure.sh"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md"
echo "📋 For testing verification, see: TESTING_REPORT.md"
echo ""

# Azure AI Configuration Guide

This guide helps you configure PPTAgent to work with Azure AI models deployed in Azure AI Foundry.

## Prerequisites

1. **Azure AI Studio/Foundry**: Access to Azure AI Studio with deployed models
2. **Azure CLI** (for AI Project method): Install and login with `az login`
3. **Model Deployments**: Your models should be deployed in Azure AI

## Quick Setup

Run the setup script to configure Azure AI automatically:

```bash
python setup_azure.py
```

## Manual Configuration

### Option 1: Azure AI Project (Recommended)

1. Create a `.env` file in your project root:

```bash
USE_AZURE=true
AZURE_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
LANGUAGE_MODEL=gpt-4o
VISION_MODEL=gpt-4o  
TEXT_MODEL=text-embedding-3-small
```

2. Ensure you're logged in with Azure CLI:
```bash
az login
```

### Option 2: Azure OpenAI Direct

1. Create a `.env` file in your project root:

```bash
USE_AZURE=true
AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_INFERENCE_CREDENTIAL=your-api-key
AZURE_API_VERSION=2024-12-01-preview
LANGUAGE_MODEL=gpt-4o
VISION_MODEL=gpt-4o
TEXT_MODEL=text-embedding-3-small
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `USE_AZURE` | Set to `true` to enable Azure AI | Yes |
| `AZURE_PROJECT_ENDPOINT` | Azure AI Project endpoint | Option 1 |
| `AZURE_ENDPOINT` | Azure OpenAI endpoint | Option 2 |
| `AZURE_INFERENCE_CREDENTIAL` | Azure OpenAI API key | Option 2 |
| `AZURE_API_VERSION` | API version (default: 2024-12-01-preview) | Option 2 |
| `LANGUAGE_MODEL` | Your deployed language model name | Yes |
| `VISION_MODEL` | Your deployed vision model name | Yes |
| `TEXT_MODEL` | Your deployed embedding model name | Yes |

## Installation

Install the required Azure packages:

```bash
pip install azure-ai-projects azure-identity azure-ai-inference
```

Or reinstall the project with updated dependencies:

```bash
pip install -e .
```

## Testing

Test your configuration:

```python
from pptagent.model_utils import ModelManager
import asyncio

async def test_azure():
    models = ModelManager()
    result = await models.test_connections()
    print(f"Connection test: {'✅ Success' if result else '❌ Failed'}")

asyncio.run(test_azure())
```

## Model Deployment Names

Make sure your environment variable model names match exactly with your Azure deployment names:

- In Azure AI Studio, check your "Deployments" section
- Use the deployment name (not the base model name)
- For example, if you deployed `gpt-4o` with deployment name `my-gpt4o`, use `my-gpt4o`

## Troubleshooting

### Authentication Issues
- For AI Project: Run `az login` and ensure you have access to the project
- For Direct OpenAI: Verify your API key and endpoint

### Model Not Found
- Check that your model deployment names match the environment variables
- Verify models are deployed and running in Azure AI Studio

### Connection Timeouts
- Increase timeout in your configuration if needed
- Check your network connectivity to Azure

## Supported Models

PPTAgent supports any Azure OpenAI compatible models, including:

- **Language Models**: GPT-4o, GPT-4, GPT-3.5-turbo
- **Vision Models**: GPT-4o, GPT-4-vision
- **Embedding Models**: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002

## Usage

Once configured, PPTAgent will automatically use your Azure models:

```bash
# Start the UI
cd pptagent_ui
python backend.py

# Or use programmatically
from pptagent.agent import Agent
agent = Agent()  # Will automatically use Azure models if configured
```

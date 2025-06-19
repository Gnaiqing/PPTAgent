#!/usr/bin/env python3
"""
Azure AI Setup Helper Script for PPTAgent

This script helps you configure PPTAgent to work with Azure AI models.
"""

import os
import sys
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("PPTAgent Azure AI Configuration Helper")
    print("=" * 60)
    print()

def check_azure_cli():
    """Check if Azure CLI is installed and user is logged in."""
    try:
        import subprocess
        result = subprocess.run(['az', 'account', 'show'], 
                              capture_output=True, text=True, check=True)
        print("✅ Azure CLI is installed and you are logged in.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Azure CLI not found or not logged in.")
        print("Please install Azure CLI and run 'az login' first.")
        print("Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
        return False

def create_env_file():
    """Create or update .env file with Azure configuration."""
    print("\nConfiguring environment variables...")
    
    env_path = Path(".env")
    
    # Get user inputs
    use_azure = input("Do you want to use Azure AI models? (y/n): ").lower().startswith('y')
    
    if not use_azure:
        with open(env_path, "w") as f:
            f.write("USE_AZURE=false\n")
        print("✅ Configured to use non-Azure models.")
        return
    
    print("\nChoose your Azure configuration method:")
    print("1. Azure AI Project (recommended)")
    print("2. Azure OpenAI Direct")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    config_lines = ["USE_AZURE=true\n"]
    
    if choice == "1":
        # Azure AI Project
        project_endpoint = input("Enter your Azure AI Project endpoint: ").strip()
        language_model = input("Enter your language model name (default: gpt-4o): ").strip() or "gpt-4o"
        vision_model = input("Enter your vision model name (default: gpt-4o): ").strip() or "gpt-4o"
        text_model = input("Enter your text embedding model name (default: text-embedding-3-small): ").strip() or "text-embedding-3-small"
        
        config_lines.extend([
            f"AZURE_PROJECT_ENDPOINT={project_endpoint}\n",
            f"LANGUAGE_MODEL={language_model}\n",
            f"VISION_MODEL={vision_model}\n",
            f"TEXT_MODEL={text_model}\n"
        ])
        
    elif choice == "2":
        # Azure OpenAI Direct
        azure_endpoint = input("Enter your Azure OpenAI endpoint: ").strip()
        api_key = input("Enter your Azure OpenAI API key: ").strip()
        api_version = input("Enter API version (default: 2024-12-01-preview): ").strip() or "2024-12-01-preview"
        language_model = input("Enter your language model deployment name (default: gpt-4o): ").strip() or "gpt-4o"
        vision_model = input("Enter your vision model deployment name (default: gpt-4o): ").strip() or "gpt-4o"
        text_model = input("Enter your text embedding model deployment name (default: text-embedding-3-small): ").strip() or "text-embedding-3-small"
        
        config_lines.extend([
            f"AZURE_ENDPOINT={azure_endpoint}\n",
            f"AZURE_INFERENCE_CREDENTIAL={api_key}\n",
            f"AZURE_API_VERSION={api_version}\n",
            f"LANGUAGE_MODEL={language_model}\n",
            f"VISION_MODEL={vision_model}\n",
            f"TEXT_MODEL={text_model}\n"
        ])
    
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Write to .env file
    with open(env_path, "w") as f:
        f.writelines(config_lines)
    
    print(f"✅ Configuration saved to {env_path}")

def install_dependencies():
    """Install Azure dependencies."""
    print("\nInstalling Azure dependencies...")
    try:
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "azure-ai-projects", "azure-identity", "azure-ai-inference"
        ])
        print("✅ Azure dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Azure dependencies.")
        print("Please run: pip install azure-ai-projects azure-identity azure-ai-inference")

def test_configuration():
    """Test the Azure configuration."""
    print("\nTesting configuration...")
    try:
        from pptagent.model_utils import ModelManager
        models = ModelManager()
        
        # Test connection
        import asyncio
        async def test():
            return await models.test_connections()
        
        result = asyncio.run(test())
        if result:
            print("✅ All model connections successful!")
            print("\n" + "=" * 60)
            print("Setup complete! You can now run PPTAgent with Azure AI models.")
            print("=" * 60)
        else:
            print("❌ Some model connections failed. Please check your configuration.")
    
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        print("Please check your environment variables and try again.")

def main():
    print_banner()
    
    # Check if Azure CLI is available (for AI Project method)
    azure_cli_available = check_azure_cli()
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration
    create_env_file()
    
    # Test configuration
    test_configuration()
    
    

if __name__ == "__main__":
    main()

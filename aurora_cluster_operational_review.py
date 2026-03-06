#!/usr/bin/env python3
"""
Aurora Cluster Review Tool

AWS Aurora cluster analysis using MCP servers and Bedrock AI
"""

import os
import sys
from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from strands_tools import shell
from strands.models import BedrockModel
from aws_session_utils import refresh_session_token_in_env
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3
import time
from datetime import datetime

# Set socket timeout globally before any network operations
import socket
socket.setdefaulttimeout(600)  # 10 minutes
os.environ["AWS_PAGER"] = ""
# Load environment variables
load_dotenv()

# Initialize app
app = BedrockAgentCoreApp()

# Global variables
aws_region = os.getenv("AWS_REGION", "us-east-1")
def create_mcp_clients():
    """Create fresh MCP client instances"""
    env = get_mcp_environment()
    def make_client(args, prefix):
        return MCPClient(
            lambda a=args: stdio_client(
                StdioServerParameters(
                    command="uvx", args=[a],
                    startup_timeout=120, env=env
                )
            ),
            prefix=prefix
        )
    return (
        make_client("awslabs.ccapi-mcp-server@latest", "cloud_"),
        make_client("awslabs.postgres-mcp-server@latest", "postgres_"),
        make_client("awslabs.cloudwatch-mcp-server@latest", "cloudwatch_"),
        make_client("awslabs.billing-cost-management-mcp-server@latest", "pricing_"),
        make_client("awslabs.aws-documentation-mcp-server@latest", "doc_"),
    )

def ensure_session_token():
    """Ensure valid session token exists"""
    session_token = os.getenv("AWS_SESSION_TOKEN")
    if not session_token or session_token == "your_aws_session_token_here" or session_token == "your_session_token_here":
        if refresh_session_token_in_env():
            print("✅ Session token ready")
        else:
            raise RuntimeError("Failed to generate session token")


def setup_bedrock_model():
    """Configure Bedrock model with extended timeout"""
    
    global bedrock_model 
    from botocore.config import Config
    
    # Configure boto client with extended timeouts
    boto_config = Config(
        read_timeout=900,  # 15 minutes
        connect_timeout=60,
        retries={
            'max_attempts': 5,
            'mode': 'adaptive'
        }
    )
    bedrock_model_id=os.getenv("BEDROCK_MODEL_ID")
    bedrock_model = BedrockModel(
        model_id=bedrock_model_id,
        max_tokens=128000,
        temperature=0.1,
        region_name=aws_region,
        boto_client_config=boto_config
    )

def get_mcp_environment():
    """Get environment variables for MCP server"""
    return {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "AWS_SESSION_TOKEN": os.getenv("AWS_SESSION_TOKEN"),
        "AWS_REGION": aws_region,
        "AWS_PAGER": "",
        "FASTMCP_LOG_LEVEL": "ERROR",
    }

def analyze_query(query: str) -> str:
    try:
        ensure_session_token()
        prompt_file = os.path.join(os.path.dirname(__file__), "cluster_review_prompt.md")
        with open(prompt_file, 'r') as f:
            prompt_template = f.read()

        system_prompt = f"""You are an AWS expert specializing in Aurora database analysis.{prompt_template}. When using the shell tool, always set non_interactive=True."""
        setup_bedrock_model()

        print("🔄 Connecting to MCP servers...")
        cloud, postgres, cloudwatch, pricing, doc = create_mcp_clients()

        with cloud, postgres, cloudwatch, pricing, doc:
            print("✅ MCP servers connected")
            tools = (
                postgres.list_tools_sync(),
                cloud.list_tools_sync(),
                cloudwatch.list_tools_sync(),
                pricing.list_tools_sync(),
                doc.list_tools_sync(),
                shell,
            )
            agent = Agent(
                model=bedrock_model,
                system_prompt=system_prompt,
                tools=tools,
            )
            result = agent(f"Analyze: {query}")
            return str(result)

    except Exception as e:
        import traceback
        return f"Analysis failed: {str(e)}\n\n{traceback.format_exc()}"

        


@app.entrypoint
async def invoke(payload):
    """Main entrypoint for Bedrock Agent Core"""
    user_input = payload.get("prompt", "")
    return analyze_query(user_input)

if __name__ == "__main__":
    print("🔥 Aurora Cluster Review Agent is Live")
    app.run(host="0.0.0.0", port=8085)
    #app.run()

# from langchain_community.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.schema import HumanMessage
from .config import config
from langchain_openai import ChatOpenAI, AzureChatOpenAI
import os
import getpass

def create_tool_chain(provider):
    if provider == 'openai':
        model_name = config.get('openai_model_name')
        api_key = config.get('openai_api_key')
        if not all([api_key, model_name]):
            raise ValueError("OpenAI API key is not set")
        return ChatOpenAI(model_name=model_name, api_key=api_key)
    elif provider == 'azure':
        # azure_endpoint = config.get('azure_openai_endpoint')
        # azure_api_key = config.get('azure_openai_api_key')
        deployment_id = config.get('azure_openai_deployment_id')
        azure_api_version = config.get('azure_openai_api_version')
        os.environ["AZURE_OPENAI_ENDPOINT"] = config.get('azure_openai_endpoint')
        os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
        config.get('azure_openai_api_key'))
        # if not all([azure_endpoint, azure_api_key, deployment_id, azure_api_version]):
        #     raise ValueError("Azure OpenAI configuration is incomplete")
        
        if not all([deployment_id, azure_api_version]):
            raise ValueError("Azure OpenAI configuration is incomplete")
        return AzureChatOpenAI(
            azure_deployment=deployment_id,
            api_version=azure_api_version
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")

def setup_langchain():
    # model_name = config.get('model_name', 'gpt-3.5-turbo')
    provider = config.get('provider', 'openai')
    return create_tool_chain(provider)

def get_chatbot_response(message):
    tool_chain = setup_langchain()
    response = tool_chain([HumanMessage(content=message)])
    return response.content

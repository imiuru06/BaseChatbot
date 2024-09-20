from langchain_community.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.schema import HumanMessage
from .config import config
from langchain_openai import ChatOpenAI

def create_tool_chain(model_name, provider):
    if provider == 'openai':
        api_key = config.get('openai_api_key')
        if not api_key:
            raise ValueError("OpenAI API key is not set")
        return ChatOpenAI(model_name=model_name, api_key=api_key)
    elif provider == 'azure':
        azure_endpoint = config.get('azure_openai_endpoint')
        azure_api_key = config.get('azure_openai_api_key')
        deployment_id = config.get('azure_openai_deployment_id')
        if not all([azure_endpoint, azure_api_key, deployment_id]):
            raise ValueError("Azure OpenAI configuration is incomplete")
        return AzureChatOpenAI(
            deployment_name=deployment_id,
            openai_api_version="2023-05-15",
            openai_api_key=azure_api_key,
            openai_api_base=azure_endpoint
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def setup_langchain():
    model_name = config.get('model_name', 'gpt-3.5-turbo')
    provider = config.get('provider', 'openai')
    return create_tool_chain(model_name, provider)

def get_chatbot_response(message):
    tool_chain = setup_langchain()
    response = tool_chain([HumanMessage(content=message)])
    return response.content

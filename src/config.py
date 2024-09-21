import os
import json
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # .env 파일에서 환경 변수 로드
        self.config = self._load_config()

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)

        # 환경 변수에서 비밀 정보 로드
        config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        config['openai_model_name'] = os.getenv('OPENAI_MODEL_NAME')

        config['azure_openai_deployment_id'] = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID')
        config['azure_openai_endpoint'] = os.getenv('AZURE_OPENAI_ENDPOINT')
        config['azure_openai_api_key'] = os.getenv('AZURE_OPENAI_API_KEY')
        config['azure_openai_api_version'] = os.getenv('AZURE_OPENAI_API_VERSION')
       
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

config = Config()

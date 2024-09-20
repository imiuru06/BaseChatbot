import os
import yaml
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self, env=None):
        load_dotenv()  # .env 파일에서 환경 변수 로드
        self.env = env or os.getenv('APP_ENV', 'development')
        self.config = self._load_config()

    def _load_config(self):
        base_path = os.path.join(os.path.dirname(__file__), 'settings')
        base_config = self._load_yaml(os.path.join(base_path, 'base.yaml'))
        env_config = self._load_yaml(os.path.join(base_path, f'{self.env}.yaml'))
        
        # 기본 설정과 환경별 설정을 병합
        config = {**base_config, **env_config}
        
        # 환경 변수에서 비밀 정보 로드
        config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        config['azure_openai_api_key'] = os.getenv('AZURE_OPENAI_API_KEY')
        
        return config

    def _load_yaml(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)

config = ConfigManager()

import os
from dotenv import load_dotenv

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        load_dotenv(".env")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.cf_endpoint_url = os.getenv("CLOUDFLARE_ENDPOINT_URL")
        self.cf_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cf_access_key_id = os.getenv("CLOUDFLARE_ACCESS_KEY_ID")
        self.cf_secret_access_key = os.getenv("CLOUDFLARE_SECRET_ACCESS_KEY")
        self.cf_bucket_name = os.getenv("CLOUDFLARE_BUCKET_NAME")

config = Config()

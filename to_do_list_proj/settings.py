from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mysql_pass : str #the setting is an env var called MYSQL_PASS - so name is important. Type: str

    model_config = SettingsConfigDict(env_file='.env') # Get the settings from .env file in dir
    
settings = Settings()
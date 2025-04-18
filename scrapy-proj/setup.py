from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, Session
from sqlalchemy import create_engine, text, String, Integer, ForeignKey, Text, MetaData
from sqlalchemy.dialects.mysql import LONGTEXT
from pydantic_settings import BaseSettings, SettingsConfigDict



# create engine, get env vars to settings. 
# create session. 
# create modules
# Base create all


class Settings(BaseSettings):
    db_password : str
    
    model_config = SettingsConfigDict(env_file=".env")


class Base(DeclarativeBase):
    pass

class Judoka(Base):
    
    __tablename__ = "judoka"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    place : Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False )
    points : Mapped[int] = mapped_column(Integer, nullable=False )


def setup():
    settings = Settings()
    
    engine = create_engine( "mysql+pymysql://ruz:" + settings.db_password + "@localhost:3306/scrapydb"
                        #    , echo=True
                        )    

    Base.metadata.create_all(engine)

    return Session(engine)
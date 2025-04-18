import requests
import json
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, Session
from sqlalchemy import create_engine, text, String, Integer, ForeignKey, Text, MetaData
from sqlalchemy.dialects.mysql import LONGTEXT
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_password : str
    
    model_config = SettingsConfigDict(env_file=".env")
    
    

my_text = requests.get("https://www.ijf.org/wrl?category=3").text
start = my_text.index("var JS_VARS =") + len("var JS_VARS =")
end = my_text[start:].index(";") + start

my_json = json.loads(my_text[start:end] )

# "family_name": "HEYDAROV")
# print(json.dumps(my_json, indent=4))
def json_find_tree(my_json , key, val) :
    
    if isinstance(my_json, list):
        for index in range(len(my_json)):
            
            res = json_find_tree( my_json[index], key, val )
            if res:
                return [index] + res       
    
    elif isinstance(my_json, dict):
        
        for (k, v) in my_json.items():
            if (k, v) == (key, val):
                return [key]
            
            res = json_find_tree( my_json[k], key, val )
            if res:
                return [k] + res 
            
    else:
        return None
        
    return None



# print( json_find_tree(my_json, "family_name", "HEYDAROV")  )

for row in my_json['preload']['wrlBrowser']['data']['rows']:
    print(row['id_person'] ,  row['place'] , row['given_name'] , row['family_name'] , row['sum_points'] )

#  'sum_points': 7254, 'place': 1
# 'id_person': '13028', 'family_name': 'HEYDAROV', 'given_name': 'Hidayat', 'gender': 'male'
# 'country_name': 'Azerbaijan'
# 'weight_name': '-73'
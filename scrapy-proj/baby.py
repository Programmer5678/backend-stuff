import requests
import json
from setup import setup
from sqlalchemy import text

my_text = requests.get("https://www.ijf.org/wrl?category=3").text
start = my_text.index("var JS_VARS =") + len("var JS_VARS =")
end = my_text[start:].index(";") + start

my_json = json.loads(my_text[start:end] )

session = setup()

for row in my_json['preload']['wrlBrowser']['data']['rows']:
    
    session.execute(text("insert into judoka values( :id_person ,  :place , CONCAT( :given_name ,  ' ', :family_name )  , :sum_points  ) "), row)


session.commit()
session.close()
from sqlalchemy import text
from setup import setup

import lorem
from random_word import RandomWords


session = setup()

r = RandomWords()


for i in range(1000):

    con = ""

    for _ in range(500):
        con += lorem.paragraph()
        con += "\n\n\n"

    session.execute( text("insert into bloglib(name, content) values( :name, :content )") ,
                    {"name" : r.get_random_word() + " " + r.get_random_word() ,
                    "content" : con} )

    # print(lorem.sentence())
    # print(lorem.paragraph()) 

session.commit()

session.close()

  
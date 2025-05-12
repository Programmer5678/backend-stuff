from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase) :
    pass


class Items(Base) :
    __tablename__ = "items"
    
    id : Mapped[int] = mapped_column( Integer, primary_key=True, autoincrement=True )
    content : Mapped[str] = mapped_column( String(100), nullable=False )
    
    
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
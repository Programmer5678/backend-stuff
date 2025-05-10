from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase) :
    pass


class Items(Base) :
    __tablename__ = "items"
    
    id : Mapped[int] = mapped_column( Integer, primary_key=True, autoincrement=True )
    content : Mapped[str] = mapped_column( String(100), nullable=False )
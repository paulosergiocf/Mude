import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine
from src.models.model_base import ModelBase
import os

from dotenv import load_dotenv
load_dotenv()

__engine: Optional[Engine] = None
global sqlite

try:
    sqlite = False if os.environ["POSTGRES"] == "True" else True
except KeyError as erro:
    sqlite = True

def create_engine() -> Engine:
    global __engine

    if __engine:
        return
    
    if sqlite:
        arquivo_db = 'data/database.sqlite'
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)

        conn_str = f'sqlite:///{arquivo_db}'
        __engine = sa.create_engine(url=conn_str, echo=False, connect_args={"check_same_thread":False}, pool_size=20, max_overflow=50, pool_timeout=60, pool_pre_ping=True, pool_recycle=3600)
        if not Path(arquivo_db).exists():
            create_tables()
    
    else:
        conn_str = f'postgresql://{os.environ["PGUSER"]}:{os.environ["PGPASSWORD"]}@{os.environ["PGHOST"]}:{os.environ["PGPORT"]}/{os.environ["PGDATABASE"]}'
        __engine = sa.create_engine(url=conn_str, echo=False)

def create_session() -> Session:
    global __engine

    if not __engine:
        create_engine()
    
    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    session: Session = __session()
    return session



def create_tables() -> None:
    global __engine
    if not __engine:
        create_engine()

    from src.models import __all__models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)

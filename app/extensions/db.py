from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
SessionLocal = scoped_session(sessionmaker())

def init_db(app):
    global engine
    engine = create_engine(app.config["DATABASE_URL"], pool_pre_ping=True)
    SessionLocal.configure(bind=engine)

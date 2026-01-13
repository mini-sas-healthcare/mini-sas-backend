from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
SessionLocal = scoped_session(sessionmaker())

def init_db(app):
    db_url = app.config.get("DATABASE_URL")

    if not db_url:
        print("WARNING: DATABASE_URL not set. DB disabled for now.")
        return

    global engine
    engine = create_engine(db_url, pool_pre_ping=True)
    SessionLocal.configure(bind=engine)

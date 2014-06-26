from . import metadata, engine

def create_db():
    metadata.create_all(engine)

def destroy_db():
    metadata.drop_all(engine)

def reset_db():
    create_db()
    destroy_db()

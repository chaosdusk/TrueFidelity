from app import app, db
from app.models import User, Label, Image, Batch

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Label': Label, 'Image': Image, 'Batch': Batch}
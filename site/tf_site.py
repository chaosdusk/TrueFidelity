from app import app, db
from app.models import User, Label, Image, Batch

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Label': Label, 'Image': Image, 'Batch': Batch, 'clear_data': clear_data}

def clear_data():
    session = db.session
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()
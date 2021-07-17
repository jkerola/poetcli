from cement import shell
from cement.utils import fs
from datetime import datetime
from . import databaseUtils


def get_all_collections(self):
    """Return all collections in the database"""
    return self.app.db.table('collections').all()


def get_all_poems_in_active_collection(self):
    """Return all poems in active collection"""
    collection = get_active_collection(self)
    return self.app.db.table(collection['name']).all()


def get_active_collection(self):
    active = databaseUtils.get_active_collection_id(self)
    return self.app.db.table('collections').get(doc_id=active)


def create_new_poem(self):
    """
    Creates a new temp file, launches editor and then returns file contents
    """
    try:
        with fs.Tmp() as tmp:
            with open(tmp.file, 'w+t') as file:
                shell.cmd(f'nano {file.name}', capture=False)
                content = file.read()
                file.close()
        if len(content.strip().strip('\n')) > 0:
            save_poem_to_active_collection(self, content)
        else:
            self.app.log.warning('Empty file detected, action aborted')
    except FileNotFoundError:
        self.app.log.error(
            'Could not create a temporary file to write in'
        )


def save_poem_to_active_collection(self, content):
    """Save poem to active collection"""
    try:
        databaseUtils.init_on_empty_collection(self)
        now = datetime.now()
        poem = {
            'created': now.strftime("%Y-%m-%d"),
            'content': content
        }
        collection = get_active_collection(self)
        self.app.db.table(collection['name']).insert(poem)
    except Exception:
        self.app.log.error('Could not save poem to database')

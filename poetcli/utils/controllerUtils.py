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
            active_id = databaseUtils.get_active_collection_id(self)
            active_col = databaseUtils.get_collection_by_id(self, active_id)
            self.app.log.info(f'Saved poem into {active_col["name"]}')
        else:
            self.app.log.warning('Empty file detected, action aborted')
    except FileNotFoundError:
        self.app.log.error(
            'Could not create a temporary file to write in'
        )


def get_poem_by_id(self, poem_id):
    """Get a poem from the database by Id"""
    try:
        col_id = databaseUtils.get_active_collection_id(self)
        collection = databaseUtils.get_collection_by_id(self, col_id)
        return self.app.db.table(collection['name']).get(doc_id=poem_id)
    except IndexError:
        self.app.log.error(f'Poem id {poem_id} not found')


def edit_poem(self, poem_id):
    """Opens poem by id in editor"""
    try:
        with fs.Tmp() as tmp:
            with open(tmp.file, 'w+t') as file:
                poem = get_poem_by_id(self, poem_id)
                previous_content = poem['content']
                file.write(previous_content)
                file.read()
                shell.cmd(f'nano {file.name}', capture=False)
                file.seek(0, 0)
                content = file.read()
                file.close()
                if len(content.strip().strip('\n')) > 0:
                    if content == previous_content:
                        self.app.log.warning(
                            'No changes detected, no actions taken'
                        )
                    else:
                        poem = {
                            'created': poem['created'],
                            'content': content
                        }
                        active = get_active_collection(self)
                        self.app.db.table(active['name']).update(
                            poem, doc_ids=[poem_id]
                        )
                        self.app.log.info('Poem updated')
                else:
                    self.app.log.warning(
                        'Empty file detected, discarding changes'
                    )
    except FileNotFoundError:
        self.app.log.error(
            'Could not create a temporary file to write in'
        )


def delete_poem(self, poem_id):
    """Delete poem permanently from active collection"""
    if get_poem_by_id(self, poem_id) is not None:
        active = get_active_collection(self)
        self.app.db.table(active['name']).remove(doc_ids=[poem_id])
        self.app.log.info(f'Deleted poem {poem_id} from {active["name"]}')
    else:
        self.app.log.error(f'Poem {poem_id} not found')


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

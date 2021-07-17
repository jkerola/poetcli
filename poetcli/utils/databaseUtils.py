import os
import random
from cement.utils import fs
from tinydb import TinyDB, Query


ADJECTIVES_PATH = 'poetcli/utils/adjectives'
NOUNS_PATH = 'poetcli/utils/nouns'


def extend_tinydb(app):
    db_file = app.config.get('poetcli', 'db_file')
    db_file = fs.abspath(db_file)

    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    TinyDB.default_table_name = 'collections'
    app.extend('db', TinyDB(db_file))

    if app.db.table('collections') == []:
        # Create a default collection
        name = generate_table_name()
        collection = app.db.table(name)
        table_reference = {'name': collection.name}
        app.db.insert(table_reference)

    if app.db.table('config').all() == []:
        # Set the default config if none exists
        config = {'active_collection': 1}
        app.db.table('config').insert(config)


def create_poem_collection(self):
    """Create a new poem collection table"""
    name = generate_table_name()
    collection = self.app.db.table(name)
    table_reference = {
        'name': collection.name
    }
    self.app.db.insert(table_reference)


def get_active_collection_id(self):
    init_on_empty_collection(self)
    return int(self.app.db.table('config').get(doc_id=1)['active_collection'])


def get_collection_by_id(self, id):
    return self.app.db.table('collections').get(doc_id=id)


def set_active_collection(self, col_id):
    try:
        col_id = int(col_id)
        init_on_empty_collection(self)
        if self.app.db.table('collections').contains(doc_id=col_id):
            self.app.db.table('config').update(
                {'active_collection': col_id},
                Query().active_collection.exists()
            )
        else:
            self.app.log.error(f'Index {col_id} does not exist')
    except ValueError:
        self.app.log.error(f"'{col_id}' is not a valid integer id")


def delete_collection(self, col_id):
    """Permanently delete collection from database"""
    try:
        col_id = int(col_id)
        if self.app.db.table('collections').contains(doc_id=col_id):
            collection = get_collection_by_id(self, col_id)
            self.app.db.drop_table(collection['name'])
            self.app.db.table('collections').remove(doc_ids=[col_id])
            if len(self.app.db.table('collections').all()) > 0:
                new_active = self.app.db.table('collections').all()[0].doc_id
                set_active_collection(self, new_active)
            init_on_empty_collection(self)
        else:
            self.app.log.error(f'Index {col_id} does not exist')
    except ValueError:
        self.app.log.error(f"'{col_id}' is not a valid integer id")


def init_on_empty_collection(self):
    """
    Creates a new collection as active if no other collections exist
    """
    if self.app.db.table('collections').all() == []:
        create_poem_collection(self)
        set_active_collection(self, 1)
        self.app.log.info('No collections found, init database')


def generate_table_name():
    """Generate a random table name as string"""
    with open(ADJECTIVES_PATH, 'r') as adjectives_file:
        adjectives = adjectives_file.readlines()
    with open(NOUNS_PATH, 'r') as nouns_file:
        nouns = nouns_file.readlines()
    adjectives_index = random.randint(0, len(adjectives) - 1)
    nouns_index = random.randint(0, len(nouns) - 1)
    chosen_adjective = adjectives[adjectives_index].rstrip('\n')
    chosen_noun = nouns[nouns_index].rstrip('\n')

    return f'{chosen_adjective} {chosen_noun}'

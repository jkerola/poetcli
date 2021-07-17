
from cement import Controller, ex
from ..utils import databaseUtils, controllerUtils


class CollectionController(Controller):
    class Meta:
        label = 'collection controls'

    @ex(
        help='set currently active collection by id or name',
        arguments=[
            (
                ['-i', '--id'],
                {
                    'help': 'collection id',
                    'action': 'store',
                    'dest': 'id'
                }
            )
        ]
    )
    def collection_active(self):
        if self.app.pargs.id is not None:
            col_id = self.app.pargs.id
            databaseUtils.set_active_collection(self, col_id)
            self.collection_list()
        else:
            col_id = databaseUtils.get_active_collection_id(self)
            collection = self.app.db.table('collections').get(doc_id=col_id)
            data = {'collection': collection}
            self.app.render(data, 'select_collection.help.jinja2')

    @ ex(help='create a new collection')
    def collection_new(self):
        databaseUtils.create_poem_collection(self)

    @ ex(help='list all collections')
    def collection_list(self):
        data = {
            'collections': controllerUtils.get_all_collections(self),
            'active_collection': databaseUtils.get_active_collection_id(self)
        }
        self.app.render(data, 'list_collections.jinja2')

    @ex(help='list all poems in active collection')
    def list(self):
        poems = controllerUtils.get_all_poems_in_active_collection(self)
        collection = controllerUtils.get_active_collection(self)
        data = {
            'poems': poems,
            'collection': collection
        }
        self.app.render(data, 'list_poems.jinja2')

    @ex(
        help='permanently delete collection',
        arguments=[
            (
                ['-i', '--id'],
                {
                    'help': 'collection id',
                    'action': 'store',
                    'dest': 'id'
                }
            )
        ]
    )
    def collection_delete(self):
        if self.app.pargs.id is not None:
            delete_id = self.app.pargs.id
            databaseUtils.delete_collection(self, delete_id)
            self.collection_list()
        else:
            self.app.render({}, 'delete_collection.help.jinja2')

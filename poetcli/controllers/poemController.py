from cement import Controller, ex
from ..utils import controllerUtils


class PoemController(Controller):
    class Meta:
        label = 'poem controls'

    @ex(help='create a new poem')
    def new(self):
        controllerUtils.create_new_poem(self)

    @ex(
        help='update existing item',
        arguments=[
            (
                ['-i', '--id'],
                {
                    'help': 'poem id',
                    'action': 'store',
                    'dest': 'poem_id'
                }
            )
        ]
    )
    def update(self):
        if self.app.pargs.poem_id is not None:
            try:
                poem_id = int(self.app.pargs.poem_id)
                controllerUtils.edit_poem(self, poem_id)
            except ValueError:
                self.app.log.error(
                    f'Id "{self.app.pargs.poem_id}" is not a number'
                )
        else:
            self.app.render({}, 'update_poem.help.jinja2')

    @ex(
        help='delete existing item',
        arguments=[
            (
                ['-i, --id'],
                {
                    'help': 'poem id',
                    'action': 'store',
                    'dest': 'poem_id'
                }
            )
        ]
    )
    def delete(self):
        if self.app.pargs.poem_id is not None:
            try:
                poem_id = int(self.app.pargs.poem_id)
                controllerUtils.delete_poem(self, poem_id)
            except ValueError:
                self.app.log.error(
                    f'Id "{self.app.pargs.poem_id}" is not a number'
                )
        else:
            self.app.render({}, 'delete_poem.help.jinja2')

    @ex(help='list all poems in active collection')
    def list(self):
        poems = controllerUtils.get_all_poems_in_active_collection(self)
        collection = controllerUtils.get_active_collection(self)
        data = {
            'poems': poems,
            'collection': collection
        }
        self.app.render(data, 'list_poems.jinja2')

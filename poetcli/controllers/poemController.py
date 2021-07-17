from cement import Controller, ex
from ..utils import controllerUtils


class PoemController(Controller):
    class Meta:
        label = 'poem controls'

    @ex(help='create a new poem')
    def new(self):
        controllerUtils.create_new_poem(self)

    @ex(help='update existing item')
    def update(self):
        pass

    @ex(help='delete existing item')
    def delete(self):
        pass

from cement import Controller, ex
from ..utils import controllerUtils


class ExportController(Controller):
    class Meta:
        label = 'export controls'

    @ex(
        help='export active collection as a file',
        arguments=[
            (
                ['-p', '--path'],
                {
                    'help': 'file path',
                    'action': 'store',
                    'dest': 'path'
                }
            )
        ]
    )
    def export(self):
        if self.app.pargs.path is not None:
            file_path = self.app.pargs.path
            active = controllerUtils.get_active_collection(self)
            file_name = active['name'].replace(' ', '_')
            poems = controllerUtils.get_all_poems_in_active_collection(self)
            if poems is not None:
                with open(f'{file_path}/{file_name}', 'w+t') as file:
                    data = {
                        'poems': poems,
                        'collection_name': active['name']
                        }
                    output = self.app.render(data, 'export.text.jinja2')
                    file.write(output)
                    print(file.read())
                    file.close()
                    self.app.log.info(
                        f'Exported into {self.app.pargs.path}/{file_name}'
                        )
            else:
                self.app.log.error('Current collection is empty')
        else:
            self.app.render({}, 'export.help.jinja2')

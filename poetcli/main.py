from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import poetCLIError
from .controllers.base import Base
from .controllers.poemController import PoemController
from .controllers.exportController import ExportController
from .controllers.collectionController import CollectionController
from .utils import databaseUtils

# configuration defaults
CONFIG = init_defaults('poetcli')
CONFIG['poetcli']['db_file'] = 'poetcli/db.json'


class PoetCLI(App):
    """poetCLI primary application."""

    class Meta:
        label = 'poetcli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            PoemController,
            CollectionController,
            ExportController
        ]

        hooks = [
            ('post_setup', databaseUtils.extend_tinydb),
        ]


class PoetCLITest(TestApp, PoetCLI):
    """A sub-class of poetCLI that is better suited for testing."""

    class Meta:
        label = 'poetcli'


def main():
    with PoetCLI() as app:
        try:
            app.run()
        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except poetCLIError as e:
            print('poetCLIError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()

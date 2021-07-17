
from cement import Controller
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
write poetry on your CLI %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'write poetry on your CLI'

        # text displayed at the bottom of --help output
        epilog = 'Usage: poetcli new'

        # controller level arguments. ex: 'poetcli --version'
        arguments = [
            # add a version banner
            (['-v', '--version'],
             {'action': 'version',
                'version': VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

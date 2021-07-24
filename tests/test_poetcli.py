from pytest import raises
from poetcli.main import PoetCLITest


def test_poetcli():
    # test poetcli without any subcommands or arguments
    with PoetCLITest() as app:
        app.run()
        assert app.exit_code == 0


def test_poetcli_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with PoetCLITest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_create_poem():
    argv = []
    with PoetCLITest(argv=argv) as app:
        app.run()
        output = app.last_rendered
        assert output is None

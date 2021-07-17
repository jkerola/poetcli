
from setuptools import setup, find_packages
from poetcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='poetcli',
    version=VERSION,
    description='write poetry on your CLI',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='jkerola',
    author_email='john.doe@example.com',
    url='https://github.com/johndoe/myapp/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'poetcli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        poetcli = poetcli.main:main
    """,
)

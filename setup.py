from setuptools import setup, find_packages
import __version__
import sys
version = __version__.version
requirements = [
    'py-deezer',
    'configset',
    'bitmath',
    'make_colors',
    'pydebugger',
    'pywget',
    'xnotify'
]

if sys.platform == 'win32':
    requirements.append('pywin32>=223')
    requirements.append('dcmd')
    requirements.append('clipboard')
    requirements.append('cefpython3')

if 'linux' in sys.platform:
    requirements.append('clipboard')
    requirements.append('cefpython3')

setup(
    name = 'deezing',
    version = version,
    author = 'Hadi Cahyadi LD',
    author_email = 'cumulus13@gmail.com',
    description = ('Download MP3 or FLAC from Deezer.com by Artist Name (for now just artist name)'),
    license = 'MIT',
    keywords = "Deezer Deemix py-deezer pydeezer",
    url = 'https://github.com/cumulus13/deez',
    scripts = [],
    py_modules = ['deez'],
    packages = find_packages(),
    download_url = 'https://github.com/cumulus13/deez/tarball/master',
    install_requires=requirements,
    # TODO
    #entry_points={
    #    "console_scripts": ["drawille=drawille:__main__"]
    #},
    entry_points = {
         "console_scripts": ["deez = deez:usage",]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

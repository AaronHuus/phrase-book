#!/usr/bin/env python
import json
import os
from datetime import datetime

from setuptools import setup, Command

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

APP_VERSION = '0.1'


class VersionCommand(Command):
    """Custom build command."""
    description = 'Generate a version.json'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import git
        repo = git.Repo(search_parent_directories=True)
        version_json = {
            'commit': repo.git.rev_parse(repo.head.object.hexsha, short=8),
            'version': APP_VERSION,
            'build_timestamp': str(datetime.utcnow()) + 'Z'
        }

        # Write to disk
        with open('%s/version.json' % CURRENT_DIR, 'w') as f:
            f.write(json.dumps(version_json))


setup(name='phrase_book',
      version=APP_VERSION,
      description='An API to support creating memorable phrases in multiple languages and storing them in books',
      author='Aaron Huus',
      author_email='ahuus1@gmail.com',
      url='https://github.com/AaronHuus/phrase-book',
      test_suite="tests",
      install_requires=[
          'GitPython==2.1.11',
          'google-cloud-translate==1.3.3',
          'Flask==1.0.2',
          'Flask-Migrate==2.4.0',
          'Flask-SQLAlchemy==2.3.2',
          'Flask-Script==2.0.6',
          'psycopg2-binary==2.7.7'
      ],
      cmdclass={
          'version': VersionCommand,
      }
      )

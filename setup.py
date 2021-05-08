import os,sys
import setuptools

setuptools.setup(
  name = 'ethermine_cli',
  packages = ['ethermine'],
  version = '1.0.0',
  url='https://github.com/KohakuBlueleaf/ethermine_cli',
  description = 'A command-line tool for monitoring the status on ethermin.',
  author = 'BlueLeaf',
  author_email = 'apolloyeh0123@gmail.com',
  zip_safe = False,
  entry_points={
    'console_scripts': [
      'ethermine = ethermine.__main__: main',
    ]
  }
)

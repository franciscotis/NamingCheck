from setuptools import setup

import naming_check.naming_check

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='naming-check',
    version=naming_check.VERSION,
    license='MIT License',
    author='Francisco Pereira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='franncisco.p@gmail.comr',
    keywords='naming check static analysis',
    description=u'A Static analysis tool for check naming conventions',
    packages=['naming_check'],
      )
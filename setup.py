from setuptools import setup


with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='naming-check',
    version='1.0.0',
    license='MIT License',
    author='Francisco Pereira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='franncisco.p@gmail.com',
    keywords='naming check static analysis',
    description=u'A Static analysis tool for check naming conventions',
    packages=['naming_check', 'naming_check.analyzers', 'naming_check.rules'],
    entry_points={
        'console_scripts': [
            'naming_check = naming_check.main:analyze'
        ]
    }
      )
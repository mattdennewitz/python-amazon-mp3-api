import os
from setuptools import setup, find_packages

from amazonmp3 import get_version


readme_copy = open(os.path.join(os.path.dirname(__file__), 
                                'README.rst')).read()

setup(
    name='python-amazon-mp3-api',
    version=get_version(),
    description='Amazon MP3 API wrapper',
    long_description=readme_copy,
    author='Matt Dennewitz',
    author_email='mattdennewitz@gmail.com',
    url='http://github.com/mattdennewitz/python-amazon-mp3-api/tree/master',
    packages=find_packages(),
    install_requires=['lxml', 'sphinx', 'httplib2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)

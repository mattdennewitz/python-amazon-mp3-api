import os
from setuptools import setup, find_packages

readme_copy = open(os.path.join(os.path.dirname(__file__), 
                                'README.rst')).read()

setup(
    name='python-amazon-mp3-api',
    version='0.0.1',
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

"""
PyIntelbras
-------------

Python Wrapper for Intelbras API
"""
import io
from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='pyintelbras',
    version='0.0.11',
    packages=['pyintelbras'],
    url='https://github.com/wiltonsr/PyIntelbras',
    license='MIT',
    author='Wilton Rodrigues',
    author_email='wiltonsr94@gmail.com',
    description='Python Wrapper for Intelbras API',
    long_description=readme,
    long_description_content_type='text/markdown',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests',
        'logging',
        'urllib3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

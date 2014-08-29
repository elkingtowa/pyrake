from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), 'pyrake/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='pyrake',
    version='0.1',
    url=' ',
    description='A high-level Python Screen Scraping framework',
    long_description=open('README.rst').read(),
    author='pyrake team',
    maintainer='Joshua Elkington',
    maintainer_email='elkingtowa@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['pyrake = pyrake.cmdline:execute']
    },
    classifiers=[
        'Framework :: pyrake',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Twisted>=10.0.0',
        'w3lib>=1.8.0',
        'queuelib',
        'lxml',
        'pyOpenSSL',
        'cssselect>=0.9',
        'six>=1.5.2',
    ],
)

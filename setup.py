from setuptools import setup, find_packages

setup(
    name='drakepost',

    version='0.0.1',

    description='Drakepost via AI BLOCKCHAIN',

    url='https://github.com/cnelson/drakepost',

    author='Chris Nelson',
    author_email='cnelson@cnelson.org',

    license='Public Domain',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: Public Domain',

        'Programming Language :: Python :: 3',
    ],

    keywords='drakepost drake like dont exploitable',

    packages=find_packages(),

    package_data={
        'drakepost': ['data/drake/*.png'],
    },

    install_requires=[
        'Pillow',
        'requests'
    ],

    entry_points={
        'console_scripts': [
            'drakepost = drakepost.drakepost:main'
        ]
    }
)

from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = [
    'spotipy'
]

setup(
    name='spotibar',
    description='Spotify plugin for Polybar',
    version='0.1.0',
    url='https://github.com/conor-f/spotibar',
    python_requires='>=3.6',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'spotibar = spotibar.client:main'
        ]
    }
)

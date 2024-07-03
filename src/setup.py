from setuptools import setup, find_packages

setup(
    name='model_synergy',
    version='0.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ModelSynergy=model_synergy.control:main',
        ],
    }
)
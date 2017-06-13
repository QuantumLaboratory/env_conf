from setuptools import setup, find_packages
from env_conf import get_version

setup(
    name="env.conf",
    version=get_version(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ]
)

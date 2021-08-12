import setuptools


setuptools.setup(
    name="shell_multiprocess",
    version="1.0.0",
    packages=["shell_multiprocess"],
    package_dir={"": "src"},
    install_requires=[
        'psutil',
        "dataclasses; python_version < '3.7'",
        "aiofiles"
    ],
    entry_points={
        'console_scripts': [
            'multiprocess = shell_multiprocess.main:main',
        ]
    }
)

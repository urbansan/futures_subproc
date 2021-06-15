import setuptools


setuptools.setup(
    name="shell_multiprocess",
    version="1.0.0",
    packages=["shell_multiprocess"],
    package_dir={"": "src"},
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'multiprocess = shell_multiprocess.scripts.multiprocess.py',
            'immuner = shell_multiprocess.scripts.multiprocess.py',
        ]
    }
)

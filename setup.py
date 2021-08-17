import setuptools


with open("long_description.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="shell_multiprocess",
    descrption="Simple shell script which runs other shell commands multi   in parallel",
    version="1.0.0",
    packages=["shell_multiprocess"],
    package_dir={"": "src"},
    install_requires=["psutil", "dataclasses; python_version < '3.7'", "aiofiles"],
    entry_points={
        "console_scripts": [
            "multiprocess = shell_multiprocess.main:main",
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

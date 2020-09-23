import setuptools


version = "0.0.4"


setuptools.setup(
    name="Pyrraform",
    version=version,
    description="Terraform SDK (to write providers)",
    long_description=open("README.rst").read(),

    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://jacquev6.github.io/Pyrraform",
    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],

    install_requires=open("requirements.txt").readlines(),
    packages=setuptools.find_packages(),
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "development/doc"),
        },
    },
)

import setuptools

setuptools.setup(
    name="Pyrraform",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=open("requirements.txt").readlines(),
)

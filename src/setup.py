import setuptools

setuptools.setup(
    name="Pyrraform",
    version="0.0.1",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ["terraform-provider-pyrraform-test=Pyrraform.test_provider:main"],
    }
)

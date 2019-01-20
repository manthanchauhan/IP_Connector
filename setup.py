import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IP_Connector",
    version="0.0.2",
    author="Manthan Chauhan",
    author_email="manthanchauhan913@gmail.com",
    description="A small example package for automatic IP Connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manthanchauhan/IP_Connector.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

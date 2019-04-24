import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prodmodel",
    version="0.0.1",
    author="Gergely Svigruha",
    author_email="gergely.svigruha@prodmodel.com",
    description="Build data science pipelines and models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prodmodel/prodmodel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "LICENSE :: OSI APPROVED :: APACHE SOFTWARE LICENSE",
        "Operating System :: OS Independent",
        "DEVELOPMENT STATUS :: 3 - ALPHA"
    ],
    entry_points={'console_scripts': ['prodmodel = prodmodel.__main__:main']}
)

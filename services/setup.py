import setuptools

#with open("../README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="Custom Python modules for getDriftlaget",
    version="0.0.1",
    author="David Berndtsson",
    author_email="david.berndtsson@gmail.com",
    description="Support modules for the main script.",
    #long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naitmare01/getDriftlaget",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
)
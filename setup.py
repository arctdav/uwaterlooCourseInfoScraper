import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uwaterlooCourseInfoScraper",
    version="1.0.1",
    author="arctdav",
    author_email="arctdav@gmail.com",
    description="This Python library scraps all UWaterloo course information from its website: \
        http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html \
        \n \
        This library only supports Python3.6+ \
        \n \
        Please do not spam their website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arctdav/UW-course-info-scraping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "bs4",
        "requests",
    ],
)
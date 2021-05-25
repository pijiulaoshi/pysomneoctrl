import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysomneoctrl",
    version="1.0.0",
    author="PijiuLaoshi",
    author_email="pijiulaoshi@gmail.com",
    description="Python package for Philips Somneo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pijiulaoshi/pysomneoctrl",
    project_urls={
        "Bug Tracker": "https://github.com/pijiulaoshi/pysomneoctrl/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

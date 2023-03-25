import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ludopy",
    version="1.5.0",
    author="Simon L. B. Sørensen",
    author_email="simonlyckbjaert@hotmail.com",
    description="A implementation of the LUDO game in python for use in AI or whatever you want",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimonLBSoerensen/LUDOpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="LUDO, game, AI",
    python_requires='>=3.8',
    license='MIT',
    install_requires=["numpy", "opencv-python>=3.1"],
    include_package_data=True,
)

#python setup.py sdist bdist_wheel
#python -m twine upload dist/*
#python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

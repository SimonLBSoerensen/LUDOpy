import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ludopy",
    version="0.0.1",
    author="Simon L. B. Sørensen",
    author_email="simonlyckbjaert@hotmail.com",
    description="LUDO python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimonLBSoerensen/LUDOpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="LUDO, game",
    python_requires='>=3.6',
    license='MIT',
    install_requires=["numpy", "opencv-python>=3.1", "tqdm"],
)

#python setup.py sdist bdist_wheel
#python -m twine upload dist/*

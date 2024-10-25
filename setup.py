from setuptools import setup, find_packages

setup(
    name="sclock",
    version="0.1.0",
    author="templedux",
    author_email="edux98g@gmail.com",
    description="Vanilla python clock implementation for easy measurement of functions and with blocks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TempledUX/PyClock",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

from setuptools import find_packages, setup

setup(
    name="LMS",
    version="1.0",
    author="Team Unity",
    url="https://github.com/uoeo-team-unity/lms",
    description="LMS Application",
    python_requires=">=3.11",
    packages=find_packages(),
    py_modules=["lms"],
)

from setuptools import find_packages, setup


setup(
    name='MCQ_GENERATOR',
    version='0.1.0',
    author='OM',
    author_email = "omchiddarwar1245@gmail.com",
    install_requires=['langchain', 'streamlit', 'PyPDF2', 'python-dotenv'],
    packages=find_packages())
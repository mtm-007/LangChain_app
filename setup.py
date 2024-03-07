from setuptools import find_packages,setup

setup(
    name="LangChainApp",
    version= '0.0.1',
    author="Merhawi_mtm007",
    author_email="-----",
    install_requires = ['langchain','streamlit','python-dotenv','pandas', 'PyPDF2','openai'],
    packages=find_packages()
)

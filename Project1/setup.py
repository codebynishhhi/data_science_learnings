# This setup.py will be responsible in building my entire machine learning application as a package
# From the setup.py anyone do the installations & start the application

from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e.'
def get_requirements(file_path:str) -> List[str]:
    ''' This function will return a list of requirements '''
    requirements = []
    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        # on iterating over each req in the requirements file it adds a \n, so we remove that 
        #  read the object & remove \n
        requirements = [req.replace("\n", "")for req in requirements]

        # -e. of requirements.txt should not run here in the setup.py 
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements





setup(
    name='mlproject_1',
    version='0.0.1',
    author='Nishi',
    author_email='nishhhi.tech@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)


# how will the setup file know the src folder of the application needs to be in the package?
#  - using __init__.py 
# the setup.py checks for all the folders that have __init__.py  
#       - entire project ---> inside the src folder 
#       - considers this as the source package itself & builds the package 
#       - once the package builds it can be imported anywhere
from setuptools import setup, find_packages

# Version Sequence [stable.beta.branch]
setup(
    name= 'menuize',
    version= '0.1.0',
    author= 'Copper Panda Consulting',
    author_email= 'ajmarcus@copper-panda.consult',
    description= 'Console-based hierarchical menu operator.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages= find_packages(),
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3'
    ],
    install_requires= [
        'logging',
        'os',
        'pickle',
        're',
        'types'
    ],
    python_requires= '>= 3.11'
)
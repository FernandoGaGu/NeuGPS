from setuptools import find_packages, setup

setup(
    name='neugps',
    author='Fernando García Gutiérrez',
    description='Implementation of the decision tree-based classification models presented in Diagnosis of Alzheimer’s '
                'disease and behavioral variant frontotemporal dementia with machine learning-aided neuropsychological'
                ' assessment using feature engineering and genetic algorithms',
    packages=find_packages(include='neugps'),
    author_email='fegarc05@ucm.es',
    version='0.1.0',
    install_requires=[
        'pandas',
        'pyarrow',
        'plotly'
    ]

)

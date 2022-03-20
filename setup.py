from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Update rules bayesian',
    ext_modules=cythonize("update_rules.pyx"),
    zip_safe=False,
)
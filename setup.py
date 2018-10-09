from __future__ import division
import os
from setuptools import setup, Extension, find_packages

from Cython.Build import cythonize
import numpy as np

flags = "-O2 -march=native -pipe -mtune=native".split()

extensions = [Extension('proq4.parse_alignments', ['proq4/parse_alignments.pyx'],
                        include_dirs=[np.get_include()], extra_compile_args=flags, extra_link_args=flags)]

setup(
    name='proq4',
    version='0.1',
    description='',
    url='https://github.com/ElofssonLab/ProQ4',
    author='David Menéndez Hurtado',
    author_email='davidmenhur@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    include_dirs=[np.get_include()],
    package_data={'proq4.models': ['proq4/models/pq4_v1.h5']},
    include_package_data=True,
    ext_modules=cythonize(extensions),
    install_requires=open('requirements.txt').read().splitlines(),
    setup_requires=['numpy', 'Cython'],
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: '
        'GNU General Public License v3 (GPLv3)'
    ],
    zip_safe=False)

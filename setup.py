#!/usr/bin/env python2

from setuptools import setup

setup(
    name='NVMeshSDK',
    version="2.3.0",
    author='Excelero, Inc.',
    url='https://github.com/excelero-sdk/NVMeshSDK',
    license='MIT', 
    description='Excelero NVMesh NVMeshSDK',
    long_description='',
    long_description_content_type='text/markdown',
    author_email='info@excelero.com',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    packages=['NVMeshSDK','NVMeshSDK.APIs','NVMeshSDK.Entities'],
    install_requires=[
                      'requests',
                      'urllib3'],

)

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='prodmodel',
    version='0.1.3',
    author='Gergely Svigruha',
    author_email='gergely.svigruha@prodmodel.com',
    description='Build data science pipelines and models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/prodmodel/prodmodel',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
    ],
    entry_points={'console_scripts': ['prodmodel = prodmodel.__main__:main']}
)

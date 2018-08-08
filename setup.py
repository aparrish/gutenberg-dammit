from setuptools import setup
    
with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='gutenbergdammit',
    version='0.0.1',
    author='Allison Parrish',
    author_email='allison@decontextualize.com',
    url='https://github.com/aparrish/gutenbergdammit',
    description='Extract plain text and metadata from the GutenTag dump',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        'Programming Language :: Python',
        "License :: OSI Approved :: MIT License",
    ],
    platforms='any',
)

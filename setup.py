from setuptools import setup, Extension


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='ujq',         # How you named your package folder (MyLib)
    packages=['ujq'],   # Chose the same as "name"
    version='2.0',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Universal Job Queue or UJQ in short is a Redis based Simple MultiPlatform Job management library build. This Library is light weight and build for working with microservices.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Krishna Raj K',                   # Type in your name
    author_email='krishnaraj2003@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Krishnaraj2003/PyUJQ',
    download_url = 'https://github.com/Krishnaraj2003/PyUJQ/archive/v2.0.0.tar.gz',
    # I explain this later on
    keywords=['UJQ', 'Redis', 'ujq', 'micro services', 'microservice',
              'redis queue', 'queue management'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'redis',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

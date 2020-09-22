
from distutils.core import setup
setup(
  name = 'UJQ',         # How you named your package folder (MyLib)
  packages = ['UJQ'],   # Chose the same as "name"
  version = '2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Universal Job Queue or UJQ in short is a Redis based Simple MultiPlatform Job management library build. This Library is light weight and build for working with microservices.',   # Give a short description about your library
  author = 'Krishna Raj K',                   # Type in your name
  author_email = 'krishnaraj2003@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Krishnaraj2003/PyUJQ',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['UJQ', 'Redis', 'ujq', 'micro services', 'microservice', 'redis queue', 'queue management'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'redis',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
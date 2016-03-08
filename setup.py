from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


setup(name='dgit_extensions',
      version='0.1',
      description='dgit addons',
      url='http://github.com/pingali/dgit-extensions',
      author='Venkata Pingali',
      author_email='pingali@gmail.com',
      license='MIT',
      keywords="dgit,addons",
      install_requires=[
          'dgit'
      ],
      packages=['dgit_extensions'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],
      entry_points = {
          'dgit.plugins': [
              'simplevalidator = dgit_extensions.simple_validator',
          ]
      },
      zip_safe=False)

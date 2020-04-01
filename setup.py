from setuptools import setup


with open('requirements/dev.txt') as f:
    install_requires = f.read().splitlines()


setup(name='PyBook',
      version='0.1.8',
      python_requires='==3.8.*',
      install_requires=install_requires,
      test_require=['pytest', 'pytest-xdist'],
      description='Flask webapp/api to gather python related content',
      url='https://gitlab.com/evagelos/PyBook',
      author='Evagelos Theodoridis',
      author_email='evagelos.theo@gmail.com',
      license='MIT'
)

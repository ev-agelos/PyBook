from setuptools import setup


with open('requirements/dev.txt') as f:
    install_requires = f.read().splitlines()


setup(name='PyBook',
      version='1.0.4',
      python_requires='==3.8.*',
      install_requires=install_requires,
      test_require=['pytest', 'pytest-xdist'],
      description='Flask webapp/api to bookmark links',
      url='https://gitlab.com/evagelos/PyBook',
      author='Evagelos Theodoridis',
      author_email='evagelos.theo@gmail.com',
      license='GLPv3'
)

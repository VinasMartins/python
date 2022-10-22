from setuptools import setup


setup(name='soccer_score',
      version='1.0',
      description='Crawler para resultados de futebol',
      url='https://github.com/VinasMartins/soccer_score/',
      author='Vinicius Pereira',
      author_email='vpmartins28@gmail.com',
      license='MIT',
      packages=['pyfutebol'],
      install_requires=[
        'beautifulsoup4',
      ],
      zip_safe=False)
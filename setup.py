from setuptools import setup

setup(name='clautoscraper'
      ,version='0.1'
      ,description='Get All Craigslist Auto Search Results for a Region'
      ,url='http://github.com/pmelgren/clautoscraper'
      ,author='Pete Melgren'
      ,author_email='pmelgren@gmail.com'
      ,license='MIT'
      ,packages=['clautoscraper']
      ,install_requires=['bs4','requests','contextlib']
      ,zip_safe=False)
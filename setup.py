from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='rtsgame',
      version='0.5',
      description='The funniest rts in the world',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      url='https://github.com/ashat1701/rts-game',
      author='Mega team',
      author_email='harmoning.moagic@ya.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pygame',
          'eventlet'
          'greenlet'
          'python-engineio'
          'requests'
          'websocket-client'
          'python-socketio'
      ],
      package_data={
          '': ["*.json", "*.png", "*.jpg"]
      },
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['rtsgame=rtsgame.MainMenu:main'],
      },
      include_package_data=True,
      zip_safe=False)

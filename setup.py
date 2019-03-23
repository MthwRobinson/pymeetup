from setuptools import setup, find_packages

reqs = ['daiquiri', 'requests']

test_reqs = ['ipython', 'pytest', 'pytest-sugar', 'pytest-cov', 'pylint']

setup(
    name='pymeetup',
    description='A Python SDK for the Meetup.com API',
    author='Matt Robinson',
    author_email='mthw.wm.robinson@gmail.com',
    packages=find_packages(),
    version='0.1.0',
    install_requires=reqs,
    extras_require={
        'test': test_reqs
    }
)


# `pymeetup`

`pymeetup` is a Python software development kit (SDK) for the Meetup.com API. I've only implemented the endpoints that I was looking to use, but if you'd like to implement more, feel free to put in a PR. See the Meetup.com API documentation for information on how to obtain an API key.

## Installation

To install `pymeetup`, clone this repo, navigate to the root directory and then run
```
pip install -e .[test]
```
This will install `pymeetup` and all dependencies. If you want to skip the test dependencies, simply omit `[test]`. Once `pymeetup` is installed, you can run the test suite with:
```
py.test --cov=pymeetup
```

## How it works

`pymeetup` provides a wrapper around the Python `requests` library that inserts your API key in the appopriate query parameter. If you do not pass the `key` argument to the `Meetup` class, `pymeetup` will look for it in the `MEETUP_KEY` environmental variable. The following workflow will work for any Meetup endpoint. If you run `meetup=Meetup(); dir(meetup)`, you'll also get a list of wrappers that have been implemented around specific endpoints.

Example:
```
from pymeetup import Meetup

meetup = Meetup('my-key')
results = meetup.get('/myCoolOrg/events')
```

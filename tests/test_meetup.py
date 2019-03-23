""" Tests for the Meetup.com SDK """
import os

import pytest

from pymeetup import Meetup

class FakeResponse:
    def __init__(self, status_code):
        self.text = '{"parrot": "big_beak"}'
        self.status_code = status_code

def test_get_events(monkeypatch):
    fake_response = FakeResponse(200)
    monkeypatch.setattr('requests.get', lambda x: fake_response)
    meetup = Meetup(key='fake_key')
    events = meetup.get_events('fake_group', page=1000, 
                               scroll='future_or_past',
                               no_earlier_than='2010-05-02',
                               no_later_than='2019-04-01')
    assert isinstance(events, dict)

def test_get_group(monkeypatch):
    fake_response = FakeResponse(200)
    monkeypatch.setattr('requests.get', lambda x: fake_response)
    meetup = Meetup(key='fake_key')
    events = meetup.get_group('fake_group', fields=['past_event_count'])
    assert isinstance(events, dict)

def test_get_event_rsvps(monkeypatch):
    fake_response = FakeResponse(200)
    monkeypatch.setattr('requests.get', lambda x: fake_response)
    meetup = Meetup(key='fake_key')
    events = meetup.get_event_rsvps('fake_group', 8675309, response='yes')
    assert isinstance(events, dict)

def test_meepup_does_not_warn_if_good_status(monkeypatch):
    fake_response = FakeResponse(200)
    monkeypatch.setattr('requests.get', lambda x: fake_response)
    meetup = Meetup(key='fake_key')
    response = meetup.get('/fake')
    assert isinstance(response, dict)

def test_meetup_warns_if_bad_status(monkeypatch):
    fake_response = FakeResponse(404)
    monkeypatch.setattr('requests.get', lambda x: fake_response)
    meetup = Meetup(key='fake_key')
    with pytest.warns(None):
        meetup.get('/fake')

def test_meetup_accepts_key_input():
    meetup = Meetup(key='fake_key')

def test_error_raises_if_no_key():
    os.environ['MEETUP_KEY'] = ""
    with pytest.raises(ValueError):
        meetup = Meetup()

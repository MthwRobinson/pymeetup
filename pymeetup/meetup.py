""" Connects to the Meetup.com API and returns results
as Python dictionaries. Users can authenticate to the Meetup.com
API using two methods:
    1. Set an environmental variable called MEETUP_KEY
    2. Pass in the key parameter when instantiating the Meetup object
"""
import json
import logging
import os
import urllib

import daiquiri
import requests

class Meetup:
    """ Pulls results from the Meetup.com API using your API key. """
    def __init__(self, key=None):
        daiquiri.setup(level=logging.INFO)
        self.logger = daiquiri.getLogger(__name__)

        if not key:
            key = os.getenv('MEETUP_KEY')
            if not key:
                msg = 'Meetup API key not provided.'
                raise ValueError(msg)
        self.key = key

        self.base_url = 'https://api.meetup.com'

    def get(self, extension, params={}):
        """ Adds the API key to the params and calls the API endpoint. """
        url = self.base_url + extension
        params['key'] = self.key
        query_params = urllib.parse.urlencode(params)
        url += '?' + query_params
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            code = response.status_code
            msg = 'API called failed with status code: {}'.format(code)
            self.logger.warning(msg)
            return {}

    def get_event_rsvps(self, urlname, event_id, response='yes,no'):
        """ Pulls a list of members who have RSVP'd for an event.
        
        Parameters
        ----------
        urlname: string
            the url name for the Meetup group (i.e. TechTalkDC)
        event_id: int
            the id for the event

        Returns
        -------
        dict, a dictionary of API results
        """
        params = {}
        params['response'] = response
        extension = '/{}/events/{}/rsvps'.format(urlname, event_id, params)
        return self.get(extension)

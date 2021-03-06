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

    def get_events(self, urlname, page=1000, scroll='future_or_past',
                   no_later_than=None, no_earlier_than=None):
        """ Pulls a list of event for the url name

        Parameters
        ----------
        urlname: str
            the url name for the Meetup group (i.e. TechTalkDC)
        page: int
            the number of results per page
        scroll: str
            determines whether or not to include past events
        not_later_than: str
            a date formatted like 'YYYY-MM-DD'
        no_earlier_than: str
            a date formatted like 'YYYY-MM-DD'

        Returns
        -------
        dict, a dictionary of API results
        """
        params = {}
        params['page'] = page
        params['scroll'] = scroll
        if no_later_than:
            params['no_later_than'] = no_later_than
        if no_earlier_than:
            params['no_earlier_than'] = no_earlier_than
        extension = '/{}/events'.format(urlname)
        return self.get(extension, params)

    def get_group(self, urlname, fields=[]):
        """ Pulls metadata about a Meetup groups

        Parameters
        ----------
        urlname: str
            the url name for the Meetup group
        fields: list
            additional fields to pull from the data

        Returns
        -------
        dict, a dictionary of API results
        """
        params = {}
        if fields:
            params['fields'] = ', '.join(fields)
        extension = '/{}'.format(urlname)
        return self.get(extension, params)

    def find_groups(self, page=20, zip_code=None, radius=None,
                    category=[], fields=[], order=None):
        """ Searches for groups near a location.

        Parameters
        ----------
        page: int
            the number of results to return
        zip_code: int
            the zip code of the location to search in
        radius: float
            how far away from the zip code centroid to search.
            minimum is 0.0 and maximum is 100.0
        category: list[int]
            a list of categories ids to serach across
            if a single int is passed, it will be converted to a list
        fields: list
            additional fields to pull from the data
        order: str
            one of ['distance', 'members', 'most_active', 'newest']
        
        Returns
        -------
        dict, a dictionary of API results
        """
        params = {}
        if page:
            params['page'] = page
        if zip_code:
            params['zip'] = zip_code
        if radius:
            params['radius'] = radius
        if category:
            if not isinstance(category, list):
                category = [category]
            category = [str(x) for x in category]
            params['category'] = ', '.join(category)
        if fields:
            params['fields'] = ', '.join(fields)
        if order:
            params['order'] = order
        extension = '/find/groups'
        return self.get(extension, params)

    def get_event_rsvps(self, urlname, event_id, response='yes,no'):
        """ Pulls a list of members who have RSVP'd for an event.
        
        Parameters
        ----------
        urlname: str
            the url name for the Meetup group (i.e. TechTalkDC)
        event_id: int
            the id for the event
        response: str
            one of ["yes,no", "yes", "no"]

        Returns
        -------
        dict, a dictionary of API results
        """
        params = {}
        params['response'] = response
        extension = '/{}/events/{}/rsvps'.format(urlname, event_id, params)
        return self.get(extension, params)

    def get_categories(self, page=50):
        """ Pulls a list of Meetup categories and their numerical IDs.

        Parameters
        ----------
        page: int
            the number of results to pull

        Returns
        -------
        dict, a dictionary of API results
        """
        params = {'page': page}
        extension = '/2/categories'
        return self.get(extension, params)

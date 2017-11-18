import json
import utils
import logging
import requests
from urlparse import urljoin

from errors import QuickpostNotFound, QuickpostSlugTaken, QuickpostNotJSON

logger = logging.getLogger('arc-cli')


class Arc():
    endpoints = {
        'content': {
            'search': 'content/v3/search'
        },
        'story': {
            'detail': 'story/v2/story/{id}'
        }
    }

    def __init__(self, env_name):
        self.env_name = env_name
        env_obj = utils.get_env(self.env_name)
        self.url = env_obj['url']
        self.key = env_obj['key']
        logger.debug('[ARC-CLI][__init__] Started with env: {}'.format(env_obj))

    def get_story_detail_url(self, id):
        return urljoin(
            self.url,
            self.endpoints['story']['detail'].format(id=id)
        )

    def search(self, params):
        payload = {
          "query": {
            "bool": {
              "must": [
              ]
            }
          }
        }

        if params.get('p2p_id'):
            payload['query']['bool']['must'].append({
              "match": {
                "source.source_id": str(params.get('p2p_id'))
              }
            })

        if params.get('canonical_url'):
            payload['query']['bool']['must'].append({
              "match": {
                "canonical_url": params.get('canonical_url')
              }
            })

        status = params.get('published', None)
        if type(status) == bool:
            payload['query']['bool']['must'].append({
              "match": {
                "published": True
              }
            })

        return self.post(
            self.endpoints['content']['search'],
            data=payload
        )

    def post(self, endpoint, data={}):
        url = urljoin(self.url, endpoint)
        logger.info('[QUICKPOST][post]: {}'.format(url))
        resp = requests.post(
            url,
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Basic {}'.format(self.key)
            }
        )
        logger.debug('[QUICKPOST][post][curl]: {}'.format(
            utils.request_to_curl(resp.request)
        ))
        return self.handle_response(resp)

    def get(self, endpoint, params={}):
        url = urljoin(self.url, endpoint)
        logger.info('[ARC-CLI][get]: {}'.format(url))
        resp = requests.get(
            url,
            params=params,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Basic {}'.format(self.key)
            }
        )
        logger.debug('[QUICKPOST][get][curl]: {}'.format(
            utils.request_to_curl(resp.request)
        ))
        return self.handle_response(resp)

    def handle_response(self, resp):
        try:
            resp.json()
            json_is_valid = True
        except ValueError as e:
            json_is_valid = False

        if resp.status_code == 404:
            raise QuickpostNotFound(resp)
        elif json_is_valid and 'p2p_htmlstory_target_slug' in resp.json() and \
resp.json()['p2p_htmlstory_target_slug'][0] == 'This slug is already in use. \
Please choose another slug.':
            raise QuickpostSlugTaken()
        else:
            logger.debug(resp.status_code)
            logger.debug(resp.content)
            resp.raise_for_status()

        try:
            return resp.json()
        except ValueError as e:
            if e.message == 'No JSON object could be decoded':
                raise QuickpostNotJSON('JSON object could be decoded: {}')

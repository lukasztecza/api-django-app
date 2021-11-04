from django.db import models
import logging
from django.conf import settings
import requests
from django.db import connection
from django.core.cache import cache


class HealthManager:
    CORRECT_NETWORK_STATUS = 'ok'
    FAIL_MESSAGE = __name__ + ' failed {0} check!'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_network(self):
        try:
            network_check_result = requests.get(settings.PARAMETERS['network_check_url']).json()
            network_check_result = network_check_result['status'] == self.CORRECT_NETWORK_STATUS
        except:
            network_check_result = False
            self.logger.error(self.FAIL_MESSAGE.format('network'))
        return network_check_result

    def check_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT count(*) FROM pg_catalog.pg_tables WHERE schemaname IN (%s, %s, %s)", ['information_schema', 'pg_catalog', 'public'])
                rows = cursor.fetchall()
                database_check_result = rows[0][0] > 0
        except:
            database_check_result = False
            self.logger.error(self.FAIL_MESSAGE.format('database'))
        return database_check_result

    def check_cache(self):
        try:
            cache.set('test_key', 'test_value', 10)
            cache_check_result = cache.get('test_key') == 'test_value'
        except:
            cache_check_result = False
            self.logger.error(self.FAIL_MESSAGE.format('cache'))
        return cache_check_result

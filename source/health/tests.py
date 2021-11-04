from django.test import TestCase
from .models import HealthManager


class HealthManagerTestCase(TestCase):
    def setUp(self):
        self.health_manager = HealthManager()

    def test_network(self):
        network_check_result = self.health_manager.check_network();
        self.assertEqual(network_check_result, True)

    def test_database(self):
        database_check_result = self.health_manager.check_database();
        self.assertEqual(database_check_result, True)

    def test_cache(self):
        cache_check_result = self.health_manager.check_cache();
        self.assertEqual(cache_check_result, True)

from rest_framework.views import APIView
from rest_framework.response import Response
from source.health.models import HealthManager


class HealthDetail(APIView):
    def get(self, request, format=None):
        health_manager = HealthManager()
        network_check_result = health_manager.check_network()
        database_check_result = health_manager.check_database()
        cache_check_result = health_manager.check_cache()

        return Response({
            'service_status': True,
            'network_status': network_check_result,
            'database_status': database_check_result,
            'cache_status': cache_check_result,
        })

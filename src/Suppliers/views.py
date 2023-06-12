from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, views, response
from rest_framework.viewsets import ModelViewSet

from django_countries import countries

from src.Suppliers.models import Suppliers

from src.Suppliers.serializers import SuppliersSerializer, CountrySerializer


class SuppliersView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = Suppliers.objects.all().order_by('id')
    serializer_class = SuppliersSerializer


class CountryListView(views.APIView):
    def get(self, request):
        country_list = []
        for code, name in countries:
            country_list.append({
                'name': name,
                'code': code
            })
        serializer = CountrySerializer(country_list, many=True)
        return response.Response(serializer.data)

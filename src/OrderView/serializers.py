from rest_framework import serializers

from src.MsSqlConnector.models import DatabaseConnection


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ["id", "database_type", "server", "database", "username"]


class ProductSerializer(serializers.Serializer):
    indeks = serializers.IntegerField()
    zlecenie = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)
    terminrealizacji = serializers.DateTimeField()

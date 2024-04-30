from rest_framework import serializers


class TaskRequestSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(min_value=1, max_value=36, default=10)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.CharField()

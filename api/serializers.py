from rest_framework import serializers

class TaskRequestSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(min_value=1, max_value=36, default=10)

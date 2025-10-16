

from rest_framework import serializers

class ShowCreateSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    screen_id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    base_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    offer = serializers.CharField(required=False, allow_null=True, allow_blank=True)

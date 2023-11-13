from rest_framework import serializers

# class LocationSerializer(serializers.Serializer):
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()

class CompareTemperaturesSerializer(serializers.Serializer):
    friend_location = serializers.CharField(allow_null=False,allow_blank=False,max_length=50)
    destination_location = serializers.CharField(allow_null=False,allow_blank=False,max_length=50)
    travel_date = serializers.DateField()
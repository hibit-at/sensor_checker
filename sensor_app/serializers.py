from rest_framework import serializers
from .models import IlluminanceData

class IlluminanceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IlluminanceData
        fields = ('timestamp', 'value')

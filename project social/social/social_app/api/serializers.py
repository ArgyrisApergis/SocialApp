from rest_framework import serializers
from .models import *

class QuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = '__all__'

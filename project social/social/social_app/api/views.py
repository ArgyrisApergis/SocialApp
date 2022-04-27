from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view

@api_view(['GET'])
def quotes(request):
    quote = Quotes.objects.all()
    quote_serialized = QuotesSerializer(quote,many= True)
    return Response(quote_serialized.data)
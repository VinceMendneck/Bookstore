from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
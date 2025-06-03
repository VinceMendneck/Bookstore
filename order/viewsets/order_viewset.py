from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from order.models import Order
from order.serializers import OrderSerializer

class OrderViewSet(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny] 
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from producto.models import Producto
from .serializers import ProductoSerializer, VentaSerializer

# Create your views here.
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='crear')
    def post(self, request, format=None):
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            new_item = serializer.save()
            return Response({'message': 'Venta creada con exito', 'data': new_item},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

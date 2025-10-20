from rest_framework import serializers
from producto.models import Producto
from venta.models import Venta
from datetime import datetime

class ProductoSerializer(serializers.ModelSerializer):
    marca = serializers.ReadOnlyField(source='marca.nombre')
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'imagen1', 'marca', 'categoria']


class VentaSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField()
    pasarela = serializers.IntegerField()
    producto = serializers.IntegerField()
    usuario = serializers.IntegerField()

    def create(self, validated_data):
        print(validated_data)
        # producto_c = Producto.objects.get(pk=self.producto)
        # total=float(producto_c.precio*self.cantidad)
        # Venta.objects.create(
        #     usuario_id=self.usuario,
        #     pasarela_id=self.pasarela,
        #     producto_id=self.producto,
        #     cantidad=self.cantidad,
        #     total=total,
        #     estatus='P',
        #     fecha=datetime.now()
        # )
        # print("venta creada")
        return validated_data

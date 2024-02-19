from django.db import models
from simple_history.models import HistoricalRecords as Historia
from core.models import ModeloBase

# Create your models here.

class Categoria(ModeloBase):
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField()
    
    class Meta:
        verbose_name_plural = 'categorias'
        
    
    def __str__(self):
        return self.nombre
    
class SucursalProveedor(ModeloBase):
    direccion = models.CharField(max_length=100)
    numero = models.CharField(max_length=20, blank=True)
    comuna = models.IntegerField(default=0)
    region = models.IntegerField(default=0)
    provincia = models.IntegerField(default=0)
    proveedor = models.ForeignKey('items.Proveedor', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'sucursales'
    
    def __str__(self):
        return self.direccion
    
def ruta_imagen_proveedor(instance, filename):
    return 'proveedor/{0}/foto/{1}'.format(instance.nombre, filename)
    
class Proveedor(ModeloBase):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    rut = models.CharField(max_length=100)
    correo = models.EmailField(max_length=255)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100)
    comuna = models.IntegerField(default=0)
    region = models.IntegerField(default=0)
    provincia = models.IntegerField(default=0)
    sucursales = models.ManyToManyField('self', through='items.SucursalProveedor')
    foto = models.ImageField(upload_to=ruta_imagen_proveedor, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'proveedores'
    
    def __str__(self):
        return self.nombre
    
    

def ruta_imagen(instance, filename):
    return 'item/{0}/foto/{1}'.format(instance.nombre, filename)
    
class Item(ModeloBase):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE, default=1)
    descripcion = models.TextField(blank=True)
    foto = models.ImageField(upload_to=ruta_imagen, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)

    proveedores = models.ManyToManyField(Proveedor, through='items.ProveedoresItem')
    
    class Meta:
        verbose_name_plural = 'items'
    

    def __str__(self):
        return self.nombre
    
class ProveedoresItem(ModeloBase):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    orden_de_compra = models.ForeignKey('ordenes_de_compra.OrdenDeCompra', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'proveedoresItem'
    
    


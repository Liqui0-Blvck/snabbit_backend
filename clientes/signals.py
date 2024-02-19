from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender='clientes.SolicitudTicket')
def creacion_ticket(sender, instance, created, **kwargs):
  if created:
    Ticket.objects.create(
      cliente = instance.cliente,
      titulo = instance.asunto,
      descripcion = instance.descripcion,
      estado = '1',
      prioridad = '1',
    )
    
@receiver(pre_save, sender=EquipoUsuario)
def actualizar_activos(sender, instance, **kwargs):
    if instance.activo:
        # Si se establece este usuario como activo, desactivar a todos los demás en el mismo equipo
        EquipoUsuario.objects.filter(equipo=instance.equipo).exclude(id=instance.id).update(activo=False)
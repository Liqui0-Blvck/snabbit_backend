from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from simple_history.utils import update_change_reason
from items.models import *


@receiver(post_save, sender='invento.Invento')
def update_change_reason(sender, instance, created, **kwargs):
    if created:
        # Si el invento es nuevo, no hay necesidad de actualizar el motivo de cambio
        return

    change_reasons = []
    for item in instance.itemeninvento_set.all():
        change_reasons.append(
            f"Se agregó el item {item.item} con una cantidad de {item.cantidad} \n"
        )

    # Obtener el historial asociado a la instancia del invento y seleccionar el primer registro
    historial = instance.historia.first()
    if historial:
        # Concatenar todos los motivos de cambio en una sola cadena
        change_reason = '\n'.join(change_reasons)
        # Actualizar el motivo de cambio en el historial
        historial.history_change_reason = change_reason
        # Guardar el historial actualizado
        historial.save()


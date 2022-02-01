from django.db.models.signals import pre_save, post_save
# from django.core.signals import request_finished
from django.dispatch import receiver
# from functools import wraps
from .models import TrainingUnit
from frequenze.models import TeacherAttendance


""" Riceve un sengnale inviato prima di salvare l'istanza di Movement """
""" Models > apps.py > init.py """

# @receiver(post_save, sender=TeacherAttendance)
def my_callback(sender, instance, **kwargs):
    hours = 0
    for attendance in TeacherAttendance.objects.filter(training_unit=instance.training_unit.pk):
        hours += attendance.hours_attended
    hours += instance.hours_attended
    uf = TrainingUnit.objects.get(pk=instance.training_unit.pk)
    uf.hours_remaining = uf.hours_expected - hours
    uf.save()

#


# def check_block_in(material, movement):
#     if movement.block_movement != 0:
#         material.block_amount_in += movement.block_movement
#         if material.block_amount_out >= movement.block_movement:
#             material.block_amount_out -= movement.block_movement
#     updated_material = material
#     return(updated_material)
#
# def check_slab_in(material, movement):
#     if movement.slab_movement != 0:
#         material.slab_amount_in += movement.slab_movement
#         if material.slab_amount_out >= movement.slab_movement:
#                 material.slab_amount_out -= movement.slab_movement
#     updated_material = material
#     return (updated_material)
#
# def material_outcoming(material, movement):
#     material.block_amount_in -= movement.block_movement
#     material.block_amount_out += movement.block_movement
#     material.slab_amount_in -= movement.slab_movement
#     material.slab_amount_out += movement.slab_movement
#     if material.storage:
#         if movement.storage:
#             material.storage += " - " + movement.storage
#     else:
#         material.storage = movement.storage
#     updated_material = material
#     return (updated_material)
#
# def material_incoming(material, movement):
#     updated_material = check_block_in(material, movement)
#     updated_material = check_slab_in(material, movement)
#     if movement.movement_reason == 1:
#         updated_material = movement.movement_date
#     return (updated_material)
#
#
# def update_description(material, movement):
#     if movement.description:
#         if material.description:
#             material.description += " - " + movement.description
#         material.description = movement.description
#     updated_material = material.description
#     return updated_material
#
# def update_block_dimensions(material, movement):
#     if movement.block_dimensions:
#         material.block_dimensions = movement.block_dimensions
#     updated_material = material.block_dimensions
#     return updated_material
#
# def update_slab_dimensions(material, movement):
#     if movement.slab_dimensions:
#         material.slab_dimensions = movement.slab_dimensions
#     updated_material = material.slab_dimensions
#     return updated_material
#
# def update_cost(material, movement):
#     if movement.cost:
#         material.cost = movement.cost
#     updated_material = material.cost
#     return updated_material
#
# def update_seller(material, movement):
#     if movement.seller:
#         material.seller = movement.seller
#     updated_material = material.seller
#     return updated_material
# def check_just_acquired(instance):
#     Movement.acquisto(Movement,
#                       instance,
#                       instance.block_amount_in,
#                       instance.slab_amount_in,
#                       instance.date_of_purchase,
#                       instance.purchase_document_number,
#                       instance.description)


#
# c
# def update_block(sender, instance, *args, **kwargs):
#     block_number = str(instance.block)
#     block = list(Block.objects.filter(block_number=block_number))
#     reason = (2, 3, 5, 7)
#     if int(instance.movement_reason) in reason:
#         block[0] = material_outcoming(block[0], instance)
#     else:
#         block[0] = material_incoming(block[0], instance)
#     block[0].description = update_description(block[0], instance)
#     block[0].block_dimensions = update_block_dimensions(block[0], instance)
#     block[0].slab_dimensions = update_slab_dimensions(block[0], instance)
#     block[0].cost = update_cost(block[0], instance)
#     block[0].seller = update_seller(block[0], instance)
#
#     # block[0] = check_just_acquired(block[0])
#     # if block[0].just_acquired == 1:
#     #     block[0].just_acquired = 0
#         # block[0] = check_just_acquired(block[0])
#
#     print(block[0].just_acquired)
#     block[0].save()

"""APPUNTI: LEVA JUST ACQUIRED, METTI CHE LE DIMENSIONI SONO UN CAMPO DI TESTO"""


"""Il rischio è che la chiamata reciproca tra segnali sia ricorsiva e che poi il programma non ne esca"""

# @receiver(post_save, sender=Block)
# def check_movements(sender, instance, *args, **kwargs):
#     if instance.just_acquired == 1:
#         Movement.acquisto(Movement,
#                               instance,
#                               instance.block_amount_in,
#                               instance.slab_amount_in,
#                               instance.date_of_purchase,
#                               instance.purchase_document_number,
#                               instance.description)


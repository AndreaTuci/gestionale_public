from django.db import models
from anagrafica.models import Staff, TrainingUnit
from django.urls import reverse
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TeacherAgreement(models.Model):

    date = models.DateField(verbose_name='Data di stipula')

    employee = models.ForeignKey(Staff,
                                 on_delete=models.CASCADE,
                                 related_name='related_staff',
                                 verbose_name='Collaboratore')

    CONTRACTS = (
        ('C', 'Collaborazione/P.IVA'),
        ('P', 'Contratto a progetto'),
        ('D', 'Tempo determinato'),
        ('I', 'Tempo indeterminato'),
    )

    contract_type = models.CharField(max_length=50,
                                     choices=CONTRACTS,
                                     default='P',
                                     verbose_name="Tipo di contratto")


    school_year = models.CharField(max_length=9,
                                   help_text='aaaa/aaaa',
                                   verbose_name='Anno scolastico')

    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name='contract_related_unit',
                                      verbose_name='Unità formativa')

    start_date = models.DateField(verbose_name='Data di avvio')

    end_date = models.DateField(verbose_name='Data di conclusione')

    wage = models.FloatField(verbose_name='Compenso')

    def __str__(self):
        return f'[{self.school_year}] {self.employee} - {self.training_unit}'

    class Meta:
        verbose_name = 'Contratto docente'
        verbose_name_plural = 'Contratti docente'


class TimeCardEntry(models.Model):

    employee = models.ForeignKey(Staff,
                                 on_delete=models.CASCADE,
                                 related_name='entry_for_employee',
                                 verbose_name='Impiegato')
    entry_date = models.DateField(auto_now_add=True,
                                  verbose_name="Data")

    entry_time = models.TimeField(auto_now_add=True,
                                  verbose_name='Ora')

    IN_OUT = (
        ('E', 'Entrata'),
        ('U', 'Uscita')
    )

    in_out = models.CharField(max_length=7,
                              choices=IN_OUT,
                              default='E',
                              verbose_name='Entrata/Uscita')

    def __str__(self):
        return f'{self.employee} - {self.get_in_out_display()} del {self.entry_date}: ore {self.entry_time}'

    class Meta:
        verbose_name = 'Entrata time card'
        verbose_name_plural = 'Entrate time card'


class Warehouse(models.Model):

    barcode = models.CharField(primary_key=True,
                               max_length=64,
                               unique=True,
                               verbose_name='Codice')

    name = models.CharField(max_length=128,
                            verbose_name='Nome')

    brand = models.CharField(max_length=128,
                             null=True,
                             verbose_name='Marca')

    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Descrizione')

    DEPARTMENT = (
        ('E', 'Elettricità'),
        ('U', 'Utensileria'),
        ('I', 'Idraulica'),
        ('F', 'Ferramenta'),
    )

    department = models.CharField(max_length=50,
                                  choices=DEPARTMENT,
                                  null=True,
                                  verbose_name="Reparto")

    quantity = models.PositiveSmallIntegerField(default=0,
                                                verbose_name="Quantità in magazzino")

    price = models.FloatField(null=True,
                              verbose_name='Costo unitario')

    last_movement = models.DateField(default=timezone.now,
                                     verbose_name='Data ultimo movimento')

    def __str__(self):
        return f'{self.name} ({self.brand})'

    def get_last_movement(self):
        last_movement = Movement.objects.filter(product=self).order_by('-movement_date', '-id')[0]
        return last_movement

    class Meta:
        verbose_name = 'Materiale'
        verbose_name_plural = 'Materiali'


class Movement(models.Model):

    product = models.ForeignKey(Warehouse,
                                on_delete=models.CASCADE,
                                related_name='related_product',
                                verbose_name='Prodotto')

    MOVEMENT_TYPE = (
        ('+', 'Entrata'),
        ('-', 'Uscita'),
    )

    movement_type = models.CharField(max_length=9,
                                     choices=MOVEMENT_TYPE,
                                     verbose_name="Tipo di movimento")

    quantity = models.PositiveSmallIntegerField(default=0,
                                                verbose_name="Quantità")

    movement_date = models.DateField(default=datetime.now,
                                     verbose_name='Data')

    def __str__(self):
        return f'[{self.movement_type}] {self.product} del {self.movement_date}'

    def clean(self):
        if self.movement_type == '-':
            product = Warehouse.objects.get(barcode=self.product.barcode)
            if product.quantity - self.quantity < 0:
                raise ValidationError(
                    _('La quantità che rimane in magazzino non può essere un numero negativo')
                )

    class Meta:
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimenti'


def check_if_closed(value):
    orders = Order.objects.filter(number=value, order_placed_at__year=datetime.now().year)
    for order in orders:
        if order.closed:
            raise ValidationError(
                (f'L`ordine {value}/{datetime.now().year} è già stato chiuso'),
                params={'value': value},
            )


class Order(models.Model):

    number = models.PositiveSmallIntegerField(validators=[check_if_closed],
                                              verbose_name='Numero di ordine')
    product = models.ForeignKey(Warehouse,
                                on_delete=models.CASCADE,
                                related_name='product_ordered',
                                verbose_name='Prodotto')

    quantity = models.PositiveSmallIntegerField(verbose_name='Quantità')

    notes = models.CharField(max_length=256,
                             blank=True,
                             null=True,
                             verbose_name='Note')

    order_placed_at = models.DateTimeField(auto_now=True,
                                           verbose_name='Data di ordine')

    closed = models.BooleanField(default=False,
                                 verbose_name='Ordine chiuso')

    def __str__(self):
        return f'[{self.quantity}] {self.product}'

    class Meta:
        verbose_name = 'Ordine'
        verbose_name_plural = 'Ordini'



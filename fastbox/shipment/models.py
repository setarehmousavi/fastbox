from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Parcel(models.Model):
    DELIVERY_TYPE_CHOICES = (
        ("local", "درون شهری"),
        ("intercity", "بین شهری"),
    )

    PACKAGE_TYPE_CHOICES = (
        ("box", "بسته"),
        ("minibox", "بسته کوچک"),
        ("nobox", "بدون جعبه"),
    )

    STATUS_CHOICES = (
        ('created', 'انجام سفارش'),
        ('picked_up', 'تحویل پیک'),
        ('in_transit', 'در دست ارسال'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'کنسل شده'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_parcels'
    )
    receiver_name = models.CharField(max_length=150)
    receiver_phone = models.CharField(max_length=20)
    sender_address = models.CharField(max_length=100, default='')
    receiver_address = models.CharField(max_length=100, default='')

    # Free-text fields instead of ForeignKey
    origin_province = models.CharField(max_length=100)
    origin_city = models.CharField(max_length=100)
    destination_province = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)

    delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPE_CHOICES)
    package_type = models.CharField(max_length=10, choices=PACKAGE_TYPE_CHOICES, default="nobox")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="کیلوگرم")
    value = models.DecimalField(max_digits=10, decimal_places=0, help_text="ارزش بسته", null=True, blank=True)

    need_package = models.BooleanField(default=False)
    length = models.DecimalField(max_digits=5, decimal_places=1, help_text="cm", null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=1, help_text="cm", null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=1, help_text="cm", null=True, blank=True)

    estimated_days = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    estimated_price = models.PositiveIntegerField(null=True, blank=True)

    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Parcel {self.tracking_code} - {self.status}"

    def price_calculation(self):
        base_price = 50000 if self.delivery_type == "intercity" else 30000
        price = base_price + (self.weight * 20000)

        if self.need_package:
            price += 5000

        if self.package_type == "minibox":
            price += 10000
        elif self.package_type == "box":
            price += 15000

        if self.delivery_type == "local":
            days = 1
        else:
            days = 3 if self.weight <= 10 else 5

        self.estimated_price = int(price)
        self.estimated_days = days

        return self.estimated_days, self.estimated_price

    def save(self, *args, **kwargs):
        self.price_calculation()
        super().save(*args, **kwargs)


class TrackingEvent(models.Model):
    parcel = models.ForeignKey(Parcel, related_name='events', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Parcel.STATUS_CHOICES)
    location = models.CharField(max_length=120, blank=True)
    note = models.CharField(max_length=255, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        
        return f"{self.parcel.tracking_code} - {self.status} @ {self.occurred_at:%Y-%m-%d %H:%M}"




      
        

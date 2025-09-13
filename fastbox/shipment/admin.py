from django.contrib import admin
from shipment.models import Parcel,TrackingEvent
# Register your models here.


admin.site.register(Parcel)
admin.site.register(TrackingEvent)
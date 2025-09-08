from django.db import models

# Create your models here.
class Shipment(models.Model):
    DELIVERY_TYPE_CHOICES =(
                ("local","درون شهری")
                ("intercity","بین شهری")
      )

    PACKAGE_TYPE_DELIVERY = (
                ("box","بسته")
                ("minibox","بسته کوچک")
                ("nobox","بدون جعبه")
    )

    
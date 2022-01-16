from django.db import models

# Create your models here.


class Quote(models.Model):
    pair_code = models.CharField(max_length=10)
    pair_price = models.DecimalField(max_digits=24, decimal_places=8)
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "quote"
        app_label = "quotes"

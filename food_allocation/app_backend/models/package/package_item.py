from django.db import models


class PackageItem(models.Model):
    package = models.ForeignKey(
        "Package", on_delete=models.PROTECT, related_name="package_items"
    )
    inventory = models.ForeignKey(
        "Inventory", on_delete=models.PROTECT, related_name="package_items"
    )
    quantity = models.IntegerField()

    class Meta:
        unique_together = ("package", "inventory")

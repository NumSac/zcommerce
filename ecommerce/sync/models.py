from django.db import models

# Create your models here.


from ecommerce.settings import AUTH_USER_MODEL


class Synchronization(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(blank=True, null=True)
    origin = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="synchronizations"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("name", "created_at")

    def __str__(self):
        return self.title

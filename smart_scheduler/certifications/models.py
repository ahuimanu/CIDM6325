from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CertificationType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    renewal_days = models.PositiveIntegerField(default=365)

    def __str__(self):
        return self.name

class EmployeeCertification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certifications",
    )
    cert_type = models.ForeignKey(
        CertificationType,
        on_delete=models.CASCADE,
        related_name="grants",
    )
    issued_on = models.DateField(default=timezone.localdate)
    expires_on = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cert_type"], name="uniq_user_certtype"
            ),
        ]

    def save(self, *args, **kwargs):
        # auto-calc expires_on if blank
        if not self.expires_on and self.issued_on:
            self.expires_on = self.issued_on + timedelta(days=self.cert_type.renewal_days)
        super().save(*args, **kwargs)

    @property
    def days_until_expiry(self):
        if not self.expires_on:
            return None
        return (self.expires_on - timezone.localdate()).days

    @property
    def is_expiring_soon(self):
        days = self.days_until_expiry
        return days is not None and days <= 30

    def __str__(self):
        return f"{self.user} • {self.cert_type} (exp {self.expires_on})"



# Create your models here.

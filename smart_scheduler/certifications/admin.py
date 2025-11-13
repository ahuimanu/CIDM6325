from django.contrib import admin
from .models import CertificationType, EmployeeCertification

@admin.register(CertificationType)
class CertificationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "renewal_days")
    search_fields = ("name",)

@admin.register(EmployeeCertification)
class EmployeeCertificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "cert_type",
        "issued_on",
        "expires_on",
        "days_until_expiry_admin",
        "expiring_soon_admin",
    )
    list_filter = ("cert_type", "expires_on")
    search_fields = ("user__username", "cert_type__name")
    readonly_fields = ("issued_on", "expires_on")  # optional

    @admin.display(description="Days until expiry")
    def days_until_expiry_admin(self, obj):
        return obj.days_until_expiry

    @admin.display(boolean=True, description="Expiring ≤ 30d")
    def expiring_soon_admin(self, obj):
        return obj.is_expiring_soon





# Register your models here.

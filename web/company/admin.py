from django.contrib import admin

from company.models import Company, RentalPoint, Reservation


admin.site.register(Company)
admin.site.register(RentalPoint)
admin.site.register(Reservation)

from django.contrib import admin
from .models import StudentCard, ICCharger, TopUpHistory

admin.site.register(StudentCard)
admin.site.register(ICCharger)
admin.site.register(TopUpHistory)

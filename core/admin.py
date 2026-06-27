from django.contrib import admin
from .models import Tenant, OrganizerProfile, Event, Participant, Registration
admin.site.register(Tenant)
admin.site.register(OrganizerProfile)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Registration)

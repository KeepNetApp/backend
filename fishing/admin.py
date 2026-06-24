from django.contrib import admin
from fishing.models import Session, Catch, CatchPhoto, Species, UserSpeciesStats

admin.site.register(Session)
admin.site.register(Catch)
admin.site.register(CatchPhoto)
admin.site.register(Species)
admin.site.register(UserSpeciesStats)

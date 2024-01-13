from django.contrib import admin

# Register your models here.
from .models import Ownership
from .forms import OwnershipForm
from .models import UserProfile

class OwnershipAdmin(admin.ModelAdmin):
    form = OwnershipForm

admin.site.register(Ownership,OwnershipAdmin)
admin.site.register(UserProfile)

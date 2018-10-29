from django.contrib import admin
from .models import Recognise
# Register your models here.


class RecogniseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recognise._meta.fields]

    class Meta:
        model = Recognise


admin.site.register(Recognise, RecogniseAdmin)

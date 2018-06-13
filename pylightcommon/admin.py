from django.contrib import admin

from .models import *

admin.site.register(ConnectedSystem)
admin.site.register(EnumIOType)
admin.site.register(IO)
admin.site.register(UsedIO)

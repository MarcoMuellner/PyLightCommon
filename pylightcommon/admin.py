from django.contrib import admin

from .models import *

admin.site.register(ConnectedSystem)
admin.site.register(IOType)
admin.site.register(IO)
admin.site.register(UsedIO)

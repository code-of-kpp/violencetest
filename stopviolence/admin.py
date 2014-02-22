from django.contrib import admin
from .models import (Theme,
                     City,
                     PoliceReport,
                     BlogEntry,
                     BlogsData,
                    )

admin.site.register(Theme)
admin.site.register(City)
admin.site.register(PoliceReport)
admin.site.register(BlogEntry)
admin.site.register(BlogsData)

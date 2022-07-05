from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Tenant)
admin.site.register(Landlord)
admin.site.register(Apartment)

admin.site.register(RoomType)
admin.site.register(Amenity)
admin.site.register(HouseRule)
admin.site.register(Booking)
admin.site.register(Reviews)

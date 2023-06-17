from django.contrib import admin

from .models import User,Daily,Profile

admin.site.register(User)
admin.site.register(Daily)
admin.site.register(Profile)
from django.contrib import admin
from models import UserProfile, UserMovieSeen, UserMovieList, UserAddList

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserMovieList)
admin.site.register(UserAddList)
admin.site.register(UserMovieSeen)

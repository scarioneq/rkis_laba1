from django.contrib import admin
from .models import Post, Option, Vote

admin.site.register(Post)
admin.site.register(Option)
admin.site.register(Vote)
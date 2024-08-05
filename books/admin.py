from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(Character)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(BookRequest)
admin.site.register(UserBook)
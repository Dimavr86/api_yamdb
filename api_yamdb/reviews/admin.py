from django.contrib import admin
from .models import Review, Comment

admin.site.register(Review)
admin.site.register(Comment)


from .models import Category, Genre, Title

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)

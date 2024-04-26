from django.contrib import admin
from news.models import Article, Tag, Like, DisLike
# Register your models here.

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(DisLike)

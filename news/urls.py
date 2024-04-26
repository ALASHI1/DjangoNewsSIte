from django.contrib import admin
from django.urls import path
from news import views

urlpatterns = [
   path('',views.home,name='home'),
   path('feed',views.feed,name='feed'),
   path('article/<int:article_id>',views.article,name='article'),
   path('tag/<str:tag>',views.articles_by_tag,name='articles_by_tag'),
   path('like/<int:article_id>',views.like_an_article,name='like_an_article'),
   path('statistics',views.statistics,name='statistics'),
   path('api/article',views.ArticleAPIView.as_view(),name='api_article')
   
]

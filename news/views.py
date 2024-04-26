from django.shortcuts import render
from news.models import Article, Tag, Like,DisLike
from django.http import JsonResponse
from django.core.serializers import serialize
from news.serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import json
# Create your views here.

def home(request):
    articles = Article.objects.all()[:4]
    
    return render(request, 'home.html', {'articles':articles})


def feed(request):
    if 'limit' in request.GET:
        try:
            count = int(request.GET.get('limit', 3))  # Default to 3 if limit is not provided or invalid
            articles = Article.objects.all()[:count]
            # Serialize the queryset into JSON format
            tagss = serialize('json', Tag.objects.all(), fields=('name', 'views'))
            data = serialize('json', articles, fields=('title', 'content', 'date', 'image', 'likes', 'views', 'tags'))
            parsed_data = json.loads(data)
            parsed_tags = json.loads(tagss)
            for dat in parsed_data:
                tag_ids = [tag['pk'] for tag in parsed_tags]
                tag_names = [tag['fields']['name'] for tag in parsed_tags]
                dat_tags = dat['fields']['tags']
                dat['fields']['tags'] = [tag_names[tag_ids.index(tag_id)] for tag_id in dat_tags]
            return JsonResponse({'articles': parsed_data}, safe=False)      
        except ValueError:
            # Handle the case where the integer conversion fails
            return JsonResponse({'error': 'Invalid limit value'}, status=400)

    # If no limit is provided, default to the first 3 articles
    articles = Article.objects.all()[:3]
    return render(request, 'news/feed.html', {'articles': articles})

def article(request, article_id):
    article = Article.objects.get(id=article_id)
    countlike = article.likes.count()
    countdislike = article.dislikes.count()
    if request.method == 'POST' and request.GET.get('like'):
        like_an_article(request, article_id)
        countlike = article.likes.count()
        countdislike = article.dislikes.count()
        return JsonResponse({'countlike':countlike, 'countdislike':countdislike})
    elif request.GET.get('like'):
        countlike = article.likes.count()
        countdislike = article.dislikes.count()
        return JsonResponse({'countlike':countlike, 'countdislike':countdislike})
    elif request.method == 'POST' and request.GET.get('dislike'):
        dislike_an_article(request, article_id)
        countlike = article.likes.count()
        countdislike = article.dislikes.count()
        return JsonResponse({'countdislike':countdislike, 'countlike':countlike})
    article.views += 1
    article.save()
    return render(request, 'news/article.html', {'article':article, 'countlike':countlike, 'countdislike':countdislike})



def articles_by_tag(request, tag):
    tagv = Tag.objects.get(name=tag)
    tagv.views += 1
    tagv.save()
    articles = Article.objects.filter(tags__name=tag)
    return render(request, 'news/tagfeed.html', {'articles':articles})

def like_an_article(request, article_id):
    art = Article.objects.get(id=article_id)
    dislike = DisLike.objects.filter(article=art, user=request.user)
    if dislike:
        return
    like = Like.objects.get_or_create(article=art, user=request.user)
    art.likes.add(like[0])
    art.save()
    return 


def dislike_an_article(request, article_id):
    art = Article.objects.get(id=article_id)
    like = Like.objects.filter(article=art, user=request.user)
    if like:
        return
    dislike = DisLike.objects.get_or_create(article=art, user=request.user)
    art.dislikes.add(dislike[0])
    art.save()
    return

def statistics(request):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    total_articles = articles.count()
    total_views = 0
    for art in articles:
        total_views += art.views    
    average_views_per_article = round(total_views/total_articles, 2)
    context = {
        'total_articles':total_articles,
        'total_views':total_views,
        'average_views_per_article':average_views_per_article,
        'articles':articles,
    }
    return render(request, 'news/statistics.html', context )



class ArticleAPIView(APIView):
    serializer_class = ArticleSerializer
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response({"message":"succesfully deleted"},status=204)

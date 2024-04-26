from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    tags = models.ManyToManyField('Tag', related_name='articles', blank=True)
    likes = models.ManyToManyField('Like', related_name='likes', blank=True)
    dislikes = models.ManyToManyField('DisLike', related_name='dislikes', blank=True)
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    views = models.IntegerField(default=0) 

    def __str__(self):
        return self.name
    
    
class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email + ' likes ' + self.article.title
    
class DisLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email + ' dislikes ' + self.article.title
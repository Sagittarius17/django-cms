from django.db import models

# Create your models here.
    
class SimpleUser(models.Model):
    profile_pic = models.ImageField(upload_to='profile_imgs/', null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phn_num = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.email}"
    
    @property
    def profilePic(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url
    
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True) # upload_to='article_imgs/'
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
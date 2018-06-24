
# create object 

``` 
Django 2.0.6
from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username='admin')
post = Post(title='用户 文章',
                slug='another-post',
                body='文章内容.',
                author=user)
post.save()
Post.objects.create(title='第一篇文章', slug='one-more-post', body='第一篇文章内容', author=user)
<Post: 第一篇文章>
```


# 使用自定义模型管理器

```
class PublishedManager(models.Manager):
    # 已发行管理器
    def get_queryset(self):
        return super().get_queryset().filter(status="published")
```

``` 

class Post(models.Model):
    # ...
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
```

``` 
Post.published.filter(title__startswith='Who')
```

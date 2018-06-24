
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


# 添加标签

``` 
pip install django_taggit==0.22.2

# ---
INSTALLED_APPS = [
    # ...
    'taggit',
]


# ---
from taggit.managers import TaggableManager

class Post(models.Model):
    # ...
    tags = TaggableManager()

# ---
python manage.py makemigrations blog
python manage.py migrate  

# ---
>>> from blog.models import Post
>>> post = Post.objects.get(id=1)

>>> post.tags.add('music', 'jazz', 'django')
>>> post.tags.all()
<QuerySet [<Tag: jazz>, <Tag: music>, <Tag: django>]>
>>> post.tags.remove('django')
>>> post.tags.all()
<QuerySet [<Tag: jazz>, <Tag: music>]>

# ---
<p class="tags">Tags: {{ post.tags.all|join:", " }}</p>


# ---

def post_list(request, tag_slug=None): 
    object_list = Post.published.all() 
    tag = None 
 
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        object_list = object_list.filter(tags__in=[tag]) 
 
    paginator = Paginator(object_list, 3) # 3 posts in each page 
    page = request.GET.get('page') 
    try: 
        posts = paginator.page(page) 
    except PageNotAnInteger: 
        # If page is not an integer deliver the first page 
        posts = paginator.page(1) 
    except EmptyPage: 
        # If page is out of range deliver last page of results 
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'blog/post/list.html', {'page': page, 
                                                   'posts': posts, 
                                                   'tag': tag}) 


# ---
path('', views.post_list, name='post_list'),
path('tag/<slug:tag_slug>/',
     views.post_list, name='post_list_by_tag'),

# ---
{% include "pagination.html" with page=posts %}

# -- 
{% if tag %}
  <h2>Posts tagged with "{{ tag.name }}"</h2>
{% endif %}

# ---
<p class="tags">
  Tags:
  {% for tag in post.tags.all %}
    <a href="{% url "blog:post_list_by_tag" tag.slug %}">
      {{ tag.name }}
    </a>
    {% if not forloop.last %}, {% endif %}
  {% endfor %}
</p>
```

# 自定义模板标签

- simple_tag: Processes the data and returns a string 
- inclusion_tag: Processes the data and returns a rendered template


## simple_tag

``` 
# ---
blog/
    __init__.py
    models.py
    ...
    templatetags/
        __init__.py
        blog_tags.py



# ---

from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

# ---

{% load blog_tags %}
{% load static %}
<!DOCTYPE html>
<html>
<body>
  <div id="sidebar">
   
    <p>This is my blog. I've written {% total_posts %} posts so far.</p>
  </div>
</body>
</html>

```


## inclusion_tag


``` 
# ---
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# ---
""" latest_posts.html """

<ul>
{% for post in latest_posts %}
  <li>
    <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>


# ---
""" base.html """

<div id="sidebar">
  <h2>My blog</h2>
  <p>This is my blog. I've written {% total_posts %} posts so far.</p>

  <h3>Latest posts</h3>
  {% show_latest_posts 3 %}
</div>




# ---
from django.db.models import Count

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]

# ---
<h3>Most commented posts</h3>
{% get_most_commented_posts as most_commented_posts %}
<ul>
{% for post in most_commented_posts %}
  <li>
    <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>
```


# 自定义过滤器 (filter)

- https://daringfireball.net/projects/markdown/basics.

- pip install Markdown==2.6.11


`blog_tags.py `

``` 
from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
```

``` 
{% load blog_tags %}


{{ post.body|linebreaks }}
{{ post.body|markdown }}

{{ post.body|truncatewords:30|linebreaks }}

{{ post.body|markdown|truncatewords_html:30 }}

```

``` 
Now, open http://127.0.0.1:8000/admin/blog/post/add/ in your browser and add a post with the following body:

This is a post formatted with markdown
--------------------------------------

*This is emphasized* and **this is more emphasized**.

Here is a list:

* One
* Two
* Three

And a [link to the Django website](https://www.djangoproject.com/)
```



from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    # 已发行管理器
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "拟稿"),
        ('published', '已发行'),
    )

    title = models.CharField(max_length=200, verbose_name="标题")
    slug = models.SlugField(max_length=200,
                            unique_for_date="publish", verbose_name="糖")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="blog_posts", verbose_name="作者")
    body = models.TextField(verbose_name="内容")
    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="最后一次更改时间")
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', verbose_name="状态")

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView


from .models import Post


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 每页显示3条
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果不是整形则转到第1页
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"

    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    """详情页
    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    print(post)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

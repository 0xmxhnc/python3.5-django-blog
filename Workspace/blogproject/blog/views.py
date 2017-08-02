# Create your views here.
import markdown
from django.shortcuts import render, get_object_or_404
#引入Category类
from comments.forms import CommentForm
from .models import Post, Category

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list':post_list})
    
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #记得在顶部引入markdown模块
    post.body = markdown.markdown(post.body,
                                                                extensions=[
                                                                    'markdown.extensions.extra',
                                                                    'markdown.extensions.codehilite',
                                                                    'markdown.extensions.toc',
                                                                ])
    #记得在顶部引入CommentForm
    form = CommentForm()
    #获取这篇post下的全部评论
    comment_list = post.comment_set.all()
    
    #将文章，表单，以及文章下的评论列表作为模板变量传给detail.html模板，以便渲染相应数据
    context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
                       }
    return render(request, 'blog/detail.html', context=context)
    return render(request, 'blog/detail.html', context={'post':post})
    
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                                        created_time__month=month
                                                        )
    return render(request, 'blog/index.html', context={'post_list':post_list})
    
def category(request, pk):
    #记得在开始部分导入Category类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})
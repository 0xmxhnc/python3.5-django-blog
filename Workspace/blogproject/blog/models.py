# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

#python_2_unicode_compatible装饰器用于兼容python2
@python_2_unicode_compatible
class Category(models.Model):
    """
	Django 要求模型必须继承 models.Model类
	Category 只需要一个简单的分类名name就可以了
	CharField 指定了分类名name 的数据类型,CharField是字符型
	CharField 的max_length 参数指定其最大长度，超过这个长度的分类名不能被保存
	Django还有多种其他数据类型，可查文档。
	"""
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name 

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible        
class Post(models.Model):
    """文章数据库表稍微复杂一点，主要是涉及字段更多
    """
    
    #文章标题
    title = models.CharField(max_length=70)
    
    #文章正文使用TextField
    #储存较短字符串使用CharField,大段文字使用TextField来储存
    body = models.TextField()

    #这两个列分别表示文章的创建时间和最后一次修改时间，储存时间字段用DataTimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    
    #文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则就会报错
    #指定CharField的blank=True参数值就可以允许空值了
    excerpt = models.CharField(max_length=200,blank=True)
    
    #这是分类与标签，分类与标签的模型我们已经定义在上面
    #我们这里用不同的关联形式将文章对应的数据库表和分类，标签对应的数据库表进行关联
    #ForeignKey可以有一对多的关联关系，即一篇文章只对应一个分类，但一个分类下可以有多篇文章
    #同样，对于标签也是如此，所以用ManyToManyField，表明这是多对多的关联关系
    #我们规定文章可以没有标签，所以为tag指定了blank=True
    #查询官方文档对上面的关联类型进行更深入的理解
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    
    #文章作者，这里User是从django.contrib.auth.models导入的
    #django.contrib.auth是Django内置的应用，专门用于处理网站用户的注册，登录等流程，User是Django为我们已经写好的用户模型
    #这里我们通过ForeignKey把文章和User关联起来
    #因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系
    author = models.ForeignKey(User)
    def __str__(self):
        return self.title
        
    #自定义get_absolute_url方法
    #记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})
        
    class Meta:
        ordering = ['-created_time']
import logging
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Count
from blog.models import *
from blog.forms import *
import json

logger = logging.getLogger("blog.views")

# Create your views here.
def global_setting(request):
    # 获得分类列表（导航列表）
    catalog_list = Catalog.objects.all()

    # 栏目数据
    column_list = Column.objects.all()

    # tag数据
    tag_list = Tag.objects.all()
    # 文章归档
    # 1.先获取文章中的年份、月份
    archive_list = Article.objects.distinct_date()

    # 标语
    # slogan = Slogan.objects.all()[0]

    # 标签云
    # 文章排行榜
    # 友情链接

    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_DESC': settings.SITE_DESC,
            'SITE_URL': settings.SITE_URL,
            'WEIBO_SINA': settings.WEIBO_SINA,
            'WEIBO_TECENT': settings.WEIBO_TENCENT,
            'PRO_RSS': settings.PRO_RSS,
            'PRO_EMAIL': settings.PRO_EMAIL,
            'catalog_list': catalog_list,
            'column_list': column_list,
            'archive_list': archive_list,
            'tag_list': tag_list,
            # 'slogan_': slogan,
            }

def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

def archive(request):

    try:
        #先获取客户端提供的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())

# 按照目录分类
def catalog(request):
    try:
        catalog_id = request.GET.get('id', None)
        catalog_ = Catalog.objects.get(id=catalog_id)
        article_list = Article.objects.filter(catalog=catalog_)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'catalog.html', locals())

def tag(request):
    try:
        tag_id = request.GET.get('id', None)
        tag_ = Tag.objects.get(id=tag_id)
        article_list = Article.objects.filter(tag=tag_)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag.html', locals())

# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 8)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

def get_article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
            article.click_count += 1
            article.save()
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'article.html', locals())

# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

# 个人简历
def resume(request):
    return render(request, 'resume.html')
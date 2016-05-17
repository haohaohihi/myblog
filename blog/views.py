import logging
from django.shortcuts import render
from django.conf import settings
from blog.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

logger = logging.getLogger("blog.views")

# Create your views here.
def global_setting(request):
    # 获得分类列表（导航列表）
    category_list = Category.objects.all()

    # 广告数据
    ad_list = Ad.objects.all()

    # 文章归档
    # 1.先获取文章中的年份、月份
    archive_list = Article.objects.distinct_date()

    # 标签云
    # 文章排行榜
    # 友情链接

    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_DESC': settings.SITE_DESC,
            'category_list': category_list,
            'ad_list': ad_list,
            'archive_list': archive_list,
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
        pass
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())


# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

# coding=utf-8
from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import hashlib

register = template.Library()


def get_pages(current, left, right, nums):
    total = left+right+1
    if total >= nums:
        return range(1, nums+1)
    elif nums-total < current < nums:
        return range(nums-total+1, nums+1)
    elif current < total:
        return range(1, total + 1)
    else:
        return range(current-left, current+right+1)


@register.simple_tag(takes_context=True)
def paginator(context, object_list, count, left=3, right=3):
    p = Paginator(object_list, count)
    current_page = context['request'].GET.get('page', 1)
    try:
        current_page = int(current_page)
        pages = get_pages(current_page, left, right, p.num_pages)
        item_list = p.page(current_page).object_list
        context['item_list'] = item_list
        context['page_list'] = p.page(current_page)
    except PageNotAnInteger:
        current_page = 1
        context['item_list'] = p.page(current_page).object_list
        pages = get_pages(current_page, left, right, p.num_pages)
        item_list = p.page(current_page).object_list
        context['item_list'] = item_list
        context['page_list'] = p.page(current_page)
    except EmptyPage:
        current_page = p.num_pages
        pages = get_pages(current_page, left, right, p.num_pages)
        item_list = p.page(current_page).object_list
        context['item_list'] = item_list
        context['page_list'] = p.page(current_page)
        test = p.page(current_page)
        test.has_previous()

    context['current_page'] = current_page
    context['last_page'] = p.num_pages
    context['pages'] = pages
    context['page_first'] = pages[0]
    context['page_last'] = pages[-1]

    return ''


@register.filter(name='imgurl') # mongo数据里取出的是imgurl,md5处理后得到关联的图片文件名
def imgurl(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


@register.filter(name='getid')
def getid(obj, attr):
    result = obj['_id']
    if result:
        return result







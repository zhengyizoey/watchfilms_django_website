#coding=utf-8
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from form import UserForm, UserProfileForm, UserAddListForm
from models import UserAddList, UserMovieList, UserMovieSeen
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from random import randint
import json

conn = MongoClient()

s = '剧情 喜剧 动作 爱情 科幻 动画 悬疑 惊悚 恐怖 纪录片 短片 情色 同性 音乐 歌舞 家庭 儿童 传记 历史 战争 犯罪 西部 奇幻 冒险 灾难 武侠 古装 运动 黑色电影'
TYPES = s.split()


def index(request):
    context = {}
    context['movie_list'] = []
    context['types'] = TYPES
    if request.method == 'GET':
        movie_type = request.GET.get('type')
        q = request.GET.get('q')
        if q:  # 如果请求搜索，返回模糊搜索出的电影
            context['movie_list'] = conn['spider']['movie'].find({'title': {'$regex': q}})
            context['current_cat'] = '查询结果"{}"'.format(q)
        elif movie_type:  # 如果访问的是电影类型
            if movie_type.encode('utf-8') in context['types']:
                context['movie_list'] = conn['spider']['movie'].find({'types': movie_type})
                context['current_cat'] = movie_type
            else:
                return HttpResponse('没有这个分类')
        else:  # 如果都没有，就是访问所有电影
            context['movie_list'] = conn['spider']['movie'].find()
            context['current_cat'] = '所有电影'
    return render(request, 'watchfilm/index.html', context)


@login_required
def recommend(request):
    movie_list = []
    count = conn['spider']['movie'].find().count() - 1
    seen_id = [x.seen for x in UserMovieSeen.objects.all()]  # 已经看过的电影ID
    for x in range(7):  # 根据随机数取出电影，并剔除看过的
        random_int = randint(0, count)
        movie = conn['spider']['movie'].find().skip(random_int).next()
        if movie['_id'] not in seen_id:
            movie_list.append(movie)
    return render(request, 'watchfilm/recommend.html', {'movie_list': movie_list})


@login_required
def mylist(request):
    user = request.user
    if request.method == 'POST':  # 如果有表单提交，保存表单数据
        form = UserAddListForm(request.POST)
        if form.is_valid:
            useradd = form.save(commit=False)
            useradd.user = user
            useradd.save()
        else:
            print form.errors
    context = {}
    context['movie_results'] = []
    queries1 = UserMovieList.objects.filter(user=user)  # 查询电影这张表
    for query in queries1:
        result = conn['spider']['movie'].find_one(
            {'_id': query.movie_id}
        )
        context['movie_results'].append(result)
    queries2 = UserAddList.objects.filter(user=user)  # 查询用户自建的影视
    context['user_add_results'] = queries2
    context['UserAddListForm'] = UserAddListForm()
    return render(request, 'watchfilm/mylist.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(username=username, password=password)
        if not user:
            User = get_user_model()
            query = User.objects.filter(email__iexact=username)
            if query:
                username = query[0].username
                user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/watchfilm/')
            else:
                return HttpResponse('not active')
        else:
            return HttpResponse('not valid')
    else:
        if request.method == 'GET':
            return render(request, 'watchfilm/login.html')


def register(request):
    registered = False
    if request.method == 'POST':
        userform = UserForm(request.POST)
        userprofileform = UserProfileForm(request.POST)
        if userform.is_valid() and userprofileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            if 'picture' in request.FILES:
                userprofile.picture = request.FILES.get('picture')
            userprofile.save()
            registered = True
            return redirect('/watchfilm/login/')
        else:
            print userform.errors, userprofileform.errors
    else:
        userform = UserForm()
        userprofileform = UserProfileForm()
    return render(request, 'watchfilm/register.html', {'registered':registered, 'userform':userform, 'userprofileform':userprofileform})


@login_required
def log_out(request):
    logout(request)
    return redirect('/watchfilm/')


@csrf_exempt
def seen(request):
    if not request.user.is_authenticated():  # 如果不是登陆用户，返回信息，回调函数重定向至登陆页
        response_dict = {'authenticated': False}
        return HttpResponse(json.dumps(response_dict))
    else:  # 如果是登陆用户，处理提交的数据
        movie_id = None
        if request.method == 'POST':
            movie_id = request.POST.get('movie_id')
        if movie_id:
            UserMovieSeen.objects.get_or_create(user=request.user, seen=movie_id)
        return HttpResponse('')

# 同上，待完善
@csrf_exempt
def add_to_list(request):
    if not request.user.is_authenticated():
        response_dict = {'authenticated': False}
        return HttpResponse(json.dumps(response_dict))
    else:
        movie_id = None
        if request.method == 'POST':
            movie_id = request.POST.get('movie_id')
        if movie_id:
            UserMovieList.objects.get_or_create(user=request.user, movie_id=movie_id)
        return HttpResponse('')


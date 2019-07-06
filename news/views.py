from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.utils import timezone
from .models import *
from .forms import NewsPost
from django.contrib.auth.models import User
import re

# Create your views here.

def news(request):
    news=News.objects.all
    return render(request, "news.html", {'news':news})
    
def create(request):
    if not request.user.is_authenticated:
        return redirect('news')
    
    if request.method =="POST":
        form=NewsPost(request.POST, request.FILES)  #이렇게 하던지(views에서 고치기) model에 가서 time=(auto_now_add=True) 
        if form.is_valid():
            news = form.save(commit=False)
            news.time = timezone.now()
            news.user = request.user
            news.save()
            save_tag(news)
        return redirect("news")
         
    #create와 new함수를 합체
    elif request.method =="GET":
        form=NewsPost()
        return render(request, "new.html", {"form":form})  

def delete(request, news_id):
    news=get_object_or_404(News, pk=news_id)
    
    if not request.user.is_authenticated:
        return redirect('news') 
        
    if request.user.is_authenticated:    
        if news.user==request.user:
            news=get_object_or_404(News, pk=news_id)
            news.delete()
            return redirect('news')
        if news.user!=request.user:
            return redirect('news')

def detail(request, news_id):
    news=get_object_or_404(News, pk=news_id)
    comments = Comment.objects.filter(news=news_id)
    return render(request, "detail.html", {"news":news, "comments":comments})

def update(request, news_id):
    news=get_object_or_404(News, pk=news_id)
    
    if not request.user.is_authenticated:
        return redirect('news')    
    
    if request.method=="POST":
            news.title=request.POST['title']
            news.content=request.POST['content']
            news.save()
            return redirect('news')
        
    elif request.method =="GET":
        if news.user==request.user:
            news=get_object_or_404(News, pk=news_id)
            return render(request, "update.html", {"news":news})
            
        if news.user!=request.user:
            return redirect('news')


def comment_create(request, news_id):
    
    if not request.user.is_authenticated:
        return redirect('new')
    
    if request.method =="POST":
            comment=Comment()
            comment.content = request.POST['content']
            comment.time = timezone.now()
            comment.news=get_object_or_404(News, pk=news_id)
            comment.user=request.user
            comment.save()
            return redirect("detail", comment.news.id)   

def comment_delete(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    
    if not request.user.is_authenticated:
        return redirect('news')
    #왜 delete는 post가 아니라 get방식을 사용해야 하는가? post쓰면 에러뜸!!
        #The view news.views.comment_delete didn't return an HttpResponse object. It returned None instead.
    if request.method =="GET":  
        if comment.user==request.user:
            comment.delete()
            return redirect('detail', comment.news.id)
        #elif comment.user!=request.username:
        if comment.user!=request.user:
            return redirect('detail', comment.news.id)
        
        #elif request.method =="GET":
            #return redirect('news')
        
    
def comment_update(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    
    if not request.user.is_authenticated:
        return redirect('news')
  
    if request.method == "POST":
            comment.content=request.POST['content']
            comment.save()
            return redirect('detail', comment.news.id)
    #comment create와 comment create page 합체
    elif request.method =="GET":
        #만약 지금 로그인된 유저와 댓글쓴사람의 유저가 같다면 수정해라.
        if comment.user==request.user:
            comment=get_object_or_404(Comment, pk=comment_id)
            return render(request, "comment_update.html", {'comment':comment})
            
        if comment.user!=request.user:
            return redirect('detail', comment.news.id)
        #else: return redirect('detail', comment.news.id)
        
def warning(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    return redirect('warning')
    
    
def like(request, news_id):
    if not request.user.is_authenticated:
         return redirect('news')
    #좋아요 표시 할 글 찾기 
    news = get_object_or_404(News, id=news_id);
    #이미 좋아요 표시했는 지 확인
    obj=Like.objects.filter(news=news, user=request.user)
    # 좋아요 안했으면 좋아요
    if len(obj) == 0:
        obj = Like()
        obj.news = news
        obj.user = request.user
        obj.save()
    # 좋아요 했으면 좋아요 취소
    else:
        obj[0].delete()
    return redirect('news')
    
def is_like(news, user):
    if (len(Like.objects.filter(news=news, user=user)) != 0):
        return True;
    return False;

def search(request):
    tag = Tag.objects.filter(tag=request.GET["tag"]).first()
    newss=[]
    for hashtag in Hashtag.objects.filter(tag=tag) :
             newss.append(hashtag.news)
    return render(request, "search.html", {"newss":newss})

#def tag_list(request, tag): 
#    t = Tag.objects.get(tag=name)
#    newss = t.news_set.all()
#    return render(request,'tag_list.html',{'newss':newss,'tag':tag})
    
    
#def tag_create(content):
#    find_tags = "".join(re.findall('#\w{0,20}\s', content))
#    find_tags = re.sub("\s", "", find_tags)
#    temp_tags = re.split("#", find_tags)
#    tags = []
#    for temp_tag in temp_tags:
#        if temp_tag == '':
#            continue
#        else:
#            tag, flag = Tag.objects.get_or_create(tag=temp_tag)
#            tags.append(tag)
#    return tags
    
#def tag_url(request):
    #if tag == tag:
        #tag=url

#def hashtag(request, content):
        #태그와 글을 연결하기    
#        hashtag = Hashtag()
#        hashtag.news = news
#        hashtag.tag = tag_obj
#        hashtag.save()
    
def save_tag(news):
    content=news.content
    l1 = content.split("#")
    l2 = []
    l1.append(l1[0]) 
    #1i에 li[0]을 추가해라 
    for str in l1:
        temp = str.split(" ")[0]
        if len(temp) != 0:
            l2.append(str.split(" ")[0])
    for str in l2:
        print(str)
    #태그 저장하기
    for tag in l2:
        tag_obj = Tag.objects.filter(tag=tag)
        if not tag_obj.exists():
            tag_obj = Tag(tag=tag)
            tag_obj.save()    #Tag(tag=tag).save()로 줄일 수 있음 앞의 tag는 모델의 tag이며 뒤의 tag는 새로운 ㅅ
    #태그와 글을 연결하기    
        hashtag = Hashtag()
        hashtag.news = news
        hashtag.tag = tag_obj
        hashtag.save()
        
        

    

def link(request):
        pass    
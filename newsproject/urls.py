"""newsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import news.views
import account.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news.views.news, name="news"),
    path('create/', news.views.create, name="create"),
    path('delete/<int:news_id>', news.views.delete, name="delete"),
    path('update/<int:news_id>', news.views.update, name="update"),
    path('detail/<int:news_id>', news.views.detail, name="detail"),
    path('search/', news.views.search, name="search"),
    path('like/<int:news_id>', news.views.like, name="like"),
    #path('tag/', news.views.tag_list, name='tag_list'),
    path('comment_create/<int:news_id>', news.views.comment_create, name="comment_create"),
    path('comment_delete/<int:comment_id>', news.views.comment_delete, name="comment_delete"),
    path('comment_update/<int:comment_id>', news.views.comment_update, name="comment_update"),
    path('warning/<int:comment_id>', news.views.warning, name="comment_update"),
    path("account/sign_in", account.views.sign_in, name="sign_in"),
    path("account/sign_up", account.views.sign_up, name="sign_up"),
    path("account/sign_out", account.views.sign_out, name="sign_out"),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
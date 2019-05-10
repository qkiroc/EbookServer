"""ebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.views.static import serve
from .settings import MEDIA_ROOT
from ebookapp import views

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'^bookstore', views.bookstore),
    url(r'^bookhtml', views.bookHTML),
    url(r'^search', views.search),
    url(r'^zone', views.zone),
    url(r'^concernhtml', views.concernHTML),
    url(r'^idealcontent',views.idealContent),
    url(r'^myideal', views.myIdeal),
    url(r'^wantread', views.wantRead),
    url(r'^likeclassify', views.likeClassify),
    url(r'^login', views.login),
    url(r'^signin', views.signIn),
    url(r'^changesex', views.changeSex),
    url(r'^changename', views.changeName),
    url(r'^changesignature', views.changeSignature),
    url(r'^changepwd', views.changePWD),
    url(r'^publish$', views.publishBookIdeal),
    url(r'^getallbookideal', views.getAllBookIdeal),
    url(r'^getconcernbookideal', views.getConcernBookIdeal),
    url(r'^like',views.postLike),
    url(r'^notlike',views.postNotLike),
    url(r'^concern',views.postConcern),
    url(r'^notconcern',views.postNotConcern),
    url(r'^islike',views.isLike),
    url(r'^isconcern',views.isConcern),
    url(r'^publishcomment',views.publishComment),
    url(r'^getcomment',views.getComment),
    url(r'^getconcern$', views.getConcern),
    url(r'^getfans$', views.getFans),
    url(r'^getconcerncount', views.getConcernCount),
    url(r'^getfanscount', views.getFansCount),
    url(r'^getbooksearch', views.getBookSearch),
    url(r'^getbooks', views.getBooks),
    url(r'^publishbookcomment', views.publishBookComment),
    url(r'^getbookcomment', views.getBookComment),
    url(r'^isbooklike', views.isBookLike),
    url(r'^postbooklike', views.postBookLike),
    url(r'^postbooknotlike', views.postBookNotLike),
    url(r'^getmyideal', views.getMyIdeal),
    url(r'^deleteideal', views.deleteIdeal),
    url(r'^getwantread', views.getWantRead),
    url(r'^postlikeclassify', views.postLikeClassify),
    url(r'^getlikeclassify', views.getLikeClassify),
    url(r'^changeuserhead', views.changeUserHead),
    

]

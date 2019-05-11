from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from ebookapp.models import user,concern,bookideal,like,comment,book,bookcomment,booklike
import random
import json
import time
from PIL import Image
import os
import pdb

# Create your views here.
def bookstore(request):
	return render(request, 'bookstores.html')
def bookHTML(request):
	bookid = request.GET['bookid']
	data = {}
	try:
		re = book.objects.get(id = bookid)
		data = {
			'title'  : re.title,
			'btype'  : re.btype,
			'author' : re.author,
			'brief'  : re.brief
		}
	except Exception as e:
		raise e
	return render(request, 'book.html',data)
def search(request):
	return render(request, 'search.html')
def zone(request):
	return render(request, 'zone.html')
def concernHTML(request):
	return render(request, 'concern.html')
def wantRead(request):
	return render(request, 'wantread.html')
def likeClassify(request):
	return render(request, 'likeclassify.html')
def idealContent(request):
	idealid = request.GET['idealid']
	data = {}
	try:
		re = bookideal.objects.get(id = idealid)
		usermsg = user.objects.get(id = str(int(re.userid))) 
		data = {
			'userid'   : re.userid,
			'username' : usermsg.username,
			'userhead' : usermsg.userhead.name,
			'time'     : re.time,
			'content'  : re.content,
			'quote'    : re.quote,
			'likecount': re.likecount,
		}
		return render(request, 'idealcontent.html',data)
	except Exception as e:
		raise e
def myIdeal(request):
	return render(request, 'myideal.html')

def signIn(request):
	username = request.POST['username']
	password = request.POST['password']
	re = 1
	data = {}
	try:
		result = user.objects.create(username = username, 
								 password = password,
								 experience = 0,
								 signature = "这个人很懒，还没有设置签名",
								 sex = 2)
		data = {
			'username'  : username,
			'ebookid'   : str(result.id).zfill(10)
		}
	except Exception as e:
		re = 0
	return HttpResponse(json.dumps({'result':re,'data':data}),content_type="application/json")

def login(request):
	username = str(int(request.POST['username']))
	password = request.POST['password']
	try:
		result = user.objects.get(id = username, password = password)
		data = {
			'userid'    : str(result.id).zfill(10),
			'username'  : result.username, 
			'experience': result.experience,
			'signature' : result.signature,
			'sex'       : result.sex,
			'userhead'  : "/media/"+result.userhead.name
		}
		return HttpResponse(json.dumps({'result':1,'data':data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def changeSex(request):
	userid = request.POST['userid']
	sex = request.POST['sex']
	userid = str(int(userid))
	result = 1
	try:
		re = user.objects.get(id = userid)
		re.sex = sex
		re.save()
	except Exception as e:
		result = 0
	return HttpResponse(json.dumps({'result':result}),content_type="application/json")
def changeName(request):
	userid = request.POST['userid']
	username = request.POST['username']
	userid = str(int(userid))
	result = 1
	try:
		re = user.objects.get(id = userid)
		re.username = username
		re.save()
	except Exception as e:
		result = 0
	return HttpResponse(json.dumps({'result':result}),content_type="application/json")

def changeSignature(request):
	userid = request.POST['userid']
	signature = request.POST['signature']
	userid = str(int(userid))
	result = 1
	try:
		re = user.objects.get(id = userid)
		re.signature = signature
		re.save()
	except Exception as e:
		result = 0
	return HttpResponse(json.dumps({'result':result}),content_type="application/json")

def changePWD(request):
	userid = request.POST['userid']
	oldpwd = request.POST['oldpwd']
	password =request.POST['password']
	userid = str(int(userid))
	result = 1
	try:
		re = user.objects.get(id = userid)
		if(re.password == oldpwd):
			re.password = password
			re.save()
		else:
			result = 2
	except Exception as e:
		result = 0
	return HttpResponse(json.dumps({'result':result}),content_type="application/json") 

def publishBookIdeal(request):
	userid = request.POST['userid']
	content = request.POST['content']
	quote = request.POST['quote']
	timestamp = int(time.time() * 1000)
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		bookideal.objects.create(userid = userid,
								 content = content,
								 quote = quote,
								 time = timestamp,
								 likecount = 0)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")


def getAllBookIdeal(request):
	userid = request.GET['userid']
	page = request.GET['page']
	datas = []
	try:
		results = bookideal.objects.filter().order_by("-time")
		pages = Paginator(results,10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for data in pages.page(page):
				isconcern = 0
				islike = 0
				buserid = data.userid
				if (len(concern.objects.filter(concernuser = userid,concerneduser = buserid))):
					isconcern = 1
				if (len(like.objects.filter(userid = userid, bookidealid = data.id))):
					islike = 1
				usermsg = user.objects.get(id = str(int(data.userid)))
				datas.append({
					'idealid'  : data.id,
					"userid"   : data.userid,
					'username' : usermsg.username,
					'userhead' : "/media/"+usermsg.userhead.name,
					'time'     : data.time,
					'content'  : data.content,
					'quote'    : data.quote,
					'likecount': data.likecount,
					'isconcern': isconcern,
					'islike'   : islike
					})
			return HttpResponse(json.dumps({"result":1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({"result":0}),content_type="application/json")

def getConcernBookIdeal(request):
	userid = request.GET['userid']
	page = request.GET['page']
	datas = []
	try:
		results = bookideal.objects.filter().order_by("-time")
		pages = Paginator(results,10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for data in pages.page(page):
				islike = 0
				buserid = data.userid
				if (len(concern.objects.filter(concernuser = userid,concerneduser = buserid))):
					if (len(like.objects.filter(userid = userid, bookidealid = data.id))):
						islike = 1
					usermsg = user.objects.get(id = str(int(data.userid)))
					datas.append({
						'idealid'  : data.id,
						'username' : usermsg.username,
						'userhead' : "/media/"+usermsg.userhead.name,
						'time'     : data.time,
						'content'  : data.content,
						'quote'    : data.quote,
						'likecount': data.likecount,
						'islike'   : islike
						})
			return HttpResponse(json.dumps({"result":1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({"result":0}),content_type="application/json")
	
	

def getMyIdeal(request):
	userid = request.GET['userid']
	page = request.GET['page']
	datas = []
	try:
		res = bookideal.objects.filter(userid = userid).order_by("-time")
		pages = Paginator(res, 10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for data in pages.page(page):
				islike = 0
				if (len(like.objects.filter(userid = userid, bookidealid = data.id))):
					islike = 1
				usermsg = user.objects.get(id = str(int(data.userid)))
				datas.append({
						'idealid'  : data.id,
						'username' : usermsg.username,
						'userhead' : "/media/"+usermsg.userhead.name,
						'time'     : data.time,
						'content'  : data.content,
						'quote'    : data.quote,
						'likecount': data.likecount,
						'islike'   : islike
					})
		return HttpResponse(json.dumps({"result":1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({"result":0}),content_type="application/json")

def deleteIdeal(request):
	idealid = request.POST['idealid']
	try:
		bookideal.objects.filter(id = idealid).delete()
		return HttpResponse(json.dumps({"result":1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({"result":0}),content_type="application/json")

def postLike(request):
	userid = request.POST["userid"]
	idealid = request.POST["idealid"]
	try:
		like.objects.create(userid = userid, bookidealid = idealid)
		re = bookideal.objects.get(id = idealid)
		re.likecount = int(re.likecount) + 1
		re.save()
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postNotLike(request):
	userid = request.POST["userid"]
	idealid = request.POST["idealid"]
	try:
		like.objects.filter(userid = userid, bookidealid = idealid).delete()
		re = bookideal.objects.get(id = idealid)
		re.likecount = int(re.likecount) - 1
		re.save()
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postConcern(request):
	userid = request.POST["userid"]
	concernedid = request.POST['concernedid']
	try:
		concern.objects.create(concernuser = userid, concerneduser = concernedid)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postNotConcern(request):
	userid = request.POST["userid"]
	concernedid = request.POST['concernedid']
	try:
		concern.objects.filter(concernuser = userid, concerneduser = concernedid).delete()
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def isLike(request):
	userid = request.POST['userid']
	bookidealid = request.POST['bookidealid']
	try:
		like.objects.get(userid = userid, bookidealid= bookidealid)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def isConcern(request):
	userid = request.POST['userid']
	concerneduserid = request.POST['concerneduserid']
	try:
		concern.objects.get(concernuser = userid,concerneduser = concerneduserid)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def publishComment(request):
	userid = request.POST['userid']
	bookidealid = request.POST["bookidealid"]
	coment = request.POST['coment']
	timestamp = int(time.time() * 1000)
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		username = usermsg.username
		comment.objects.create(userid = userid, 
							   bookidealid = bookidealid,
							   time = timestamp,
							   coment = coment)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getComment(request):
	bookidealid = request.GET["bookidealid"]
	data = []
	try:
		res = comment.objects.filter(bookidealid = bookidealid)
		for re in res:
			usermsg = user.objects.get(id = str(int(re.userid)))
			data.append({
					"userid"   : re.userid, 
				    "userhead" : "/media/"+usermsg.userhead.name,
				    "username" : usermsg.username,
				    "time"     : re.time,
				    "coment"   : re.coment
				}) 
		return HttpResponse(json.dumps({'result':1,"data":data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getConcernCount(request):
	userid = request.GET['userid']
	try:
		res = concern.objects.filter(concernuser = userid)
		return HttpResponse(json.dumps({'result':1,"data":len(res)}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getFansCount(request):
	userid = request.GET['userid']
	try:
		res = concern.objects.filter(concerneduser = userid)
		return HttpResponse(json.dumps({'result':1,"data":len(res)}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getConcern(request):
	userid = request.GET['userid']
	data = []
	try:
		res = concern.objects.filter(concernuser = userid)
		for re in res:
			usermsg = user.objects.get(id = str(int(re.concerneduser)))
			data.append({
				    "userid"   : re.concerneduser,
				    "username" : usermsg.username,
				    "userhead" : "/media/"+usermsg.userhead.name,
				    "signature": usermsg.signature,
				    "isconcern": 1
 				})
			data.reverse()
		return HttpResponse(json.dumps({'result':1,"data":data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getFans(request):
	userid = request.GET['userid']
	data = []
	try:
		res = concern.objects.filter(concerneduser = userid)
		for re in res:
			isconcern = len(concern.objects.filter(concernuser = userid, concerneduser = re.concernuser))
			usermsg = user.objects.get(id = str(int(re.concernuser)))
			data.append({
				    "userid"   : re.concernuser,
				    "username" : usermsg.username,
				    "userhead" : "/media/"+usermsg.userhead.name,
				    "signature": usermsg.signature,
				    "isconcern": isconcern
 				})
			data.reverse()
		return HttpResponse(json.dumps({'result':1,"data":data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getBooks(request):
	page = request.GET['page']
	userid = request.GET['userid']
	btype = request.GET['type']
	datas = []
	try:
		if (btype == "all"):
			if len(userid):
				interest = user.objects.get(id = str(int(userid))).interest.split(",")
				if len(interest) != 0 and interest[0] != '':
					res = book.objects.filter(btype__in = interest).order_by("-id")
				else:
					res = book.objects.filter().order_by("-id")
			else:
				res = book.objects.filter().order_by("-id")
		else:
			res = book.objects.filter(btype = btype).order_by("-id")
		pages = Paginator(res, 10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for data in pages.page(page):
				datas.append({
						"id"    : data.id,
						"title" : data.title,
						"author": data.author,
						"brief" : data.brief,
						"type"  : data.btype
					})
			return HttpResponse(json.dumps({'result':1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0,"data":datas}),content_type="application/json")

def publishBookComment(request):
	userid = request.POST['userid']
	bookid = request.POST["bookid"]
	coment = request.POST['coment']
	timestamp = int(time.time() * 1000)
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		username = usermsg.username
		bookcomment.objects.create(userid = userid, 
								   bookid = bookid,
								   time = timestamp,
								   coment = coment)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getBookComment(request):
	bookid = request.GET["bookid"]
	data = []
	try:
		res = bookcomment.objects.filter(bookid = bookid)
		for re in res:
			usermsg = user.objects.get(id = str(int(re.userid)))
			data.append({
					"userid"   : re.userid, 
				    "userhead" : "/media/"+usermsg.userhead.name,
				    "username" : usermsg.username,
				    "time"     : re.time,
				    "coment"   : re.coment
				}) 
		return HttpResponse(json.dumps({'result':1,"data":data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def isBookLike(request):
	try:
		userid = request.POST['userid']
		bookid = request.POST['bookid']
		booklike.objects.get(userid = userid, bookid= bookid)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postBookLike(request):
	userid = request.POST['userid']
	bookid = request.POST['bookid']
	try:
		booklike.objects.create(userid = userid, bookid= bookid)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postBookNotLike(request):
	userid = request.POST['userid']
	bookid = request.POST['bookid']
	try:
		booklike.objects.filter(userid = userid, bookid= bookid).delete()
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getWantRead(request):
	userid = request.GET['userid']
	page = request.GET['page']
	datas = []
	try:
		res = booklike.objects.filter(userid = userid).order_by("-id")
		pages = Paginator(res, 10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for re in pages.page(page):
				data = book.objects.get(id = re.bookid)
				datas.append({
						"id"    : data.id,
						"title" : data.title,
						"author": data.author,
						"brief" : data.brief,
						"type"  : data.btype
					})
		return HttpResponse(json.dumps({'result':1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getLikeClassify(request):
	userid = request.GET['userid']
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		items = usermsg.interest.split(",")
		if items[0] == '':
			items = []

		return HttpResponse(json.dumps({'result':1,"data":items}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def postLikeClassify(request):
	userid = request.POST["userid"]
	items = request.POST['items']
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		usermsg.interest = items;
		usermsg.save()
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def getBookSearch(request):
	keyword = request.GET['keyword']
	page = request.GET['page']
	datas = []
	try:
		res = book.objects.filter(Q(title__icontains=keyword) | Q(brief__icontains=keyword))
		pages = Paginator(res, 10)
		if pages.num_pages < int(page):
			return HttpResponse(json.dumps({'result':2}),content_type="application/json")
		else:
			for data in pages.page(page):
				datas.append({
						"id"    : data.id,
						"title" : data.title,
						"author": data.author,
						"brief" : data.brief,
						"type"  : data.btype
					})
			return HttpResponse(json.dumps({'result':1,"data":datas}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def changeUserHead(request):
	img = request.POST['img']
	userid = request.POST['userid']
	import base64
	from django.core.files.base import ContentFile
	userhead = base64.b64decode(img)
	file_content = ContentFile(userhead)	
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		usermsg.userhead.save(userid+".jpg",file_content)
		return HttpResponse("/media/"+usermsg.userhead.name,content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")
	
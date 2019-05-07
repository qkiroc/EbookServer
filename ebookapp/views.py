from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import requests
from ebookapp.models import user,concern,bookideal,like,comment
import random
import json
import time
import pdb

# Create your views here.
def zone(request):
	return render(request, 'zone.html')
def concernHTML(request):
	return render(request, 'concern.html')
def idealContent(request):
	idealid = request.GET['idealid']
	data = {}
	try:
		re = bookideal.objects.get(id = idealid)
		data = {
			'userid'   : re.userid,
			'username' : re.username,
			'userhead' : re.userhead,
			'time'     : re.time,
			'content'  : re.content,
			'quote'    : re.quote,
			'likecount': re.likecount,
		}
		return render(request, 'idealcontent.html',data)
	except Exception as e:
		raise e

def signIn(request):
	username = request.POST['username']
	password = request.POST['password']
	re = 1
	data = {}
	#pdb.set_trace()
	try:
		result = user.objects.create(username = username, 
								 password = password,
								 experience = 0,
								 signature = "这个人很懒，还没有设置签名",
								 sex = 2,
								 userhead = '')
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
			'userhead'  : result.userhead
		}
		return HttpResponse(json.dumps({'result':1,'data':data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")

def changeSex(request):
	userid = request.POST['userid']
	sex = request.POST['sex']
	userid = str(int(userid))
	pdb.set_trace()
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

def  publishBookIdeal(request):
	userid = request.POST['userid']
	content = request.POST['content']
	quote = request.POST['quote']
	timestamp = int(time.time() * 1000)
	try:
		usermsg = user.objects.get(id = str(int(userid)))
		bookideal.objects.create(userid = userid,
								 username = usermsg.username,
								 userhead = usermsg.userhead,
								 content = content,
								 quote = quote,
								 time = timestamp,
								 likecount = 0)
		return HttpResponse(json.dumps({'result':1}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")


def getAllBookIdeal(request):
	userid = request.GET['userid']
	results = bookideal.objects.filter()
	datas = []
	for data in results:
		isconcern = 0
		islike = 0
		buserid = data.userid
		if (len(concern.objects.filter(concernuser = userid,concerneduser = buserid))):
			isconcern = 1
		if (len(like.objects.filter(userid = userid, bookidealid = data.id))):
			islike = 1
		datas.append({
			'idealid'  : data.id,
			"userid"   : data.userid,
			'username' : data.username,
			'userhead' : data.userhead,
			'time'     : data.time,
			'content'  : data.content,
			'quote'    : data.quote,
			'likecount': data.likecount,
			'isconcern': isconcern,
			'islike'   : islike
			})
	datas.reverse()
	return HttpResponse(json.dumps(datas),content_type="application/json")

def getConcernBookIdeal(request):
	userid = request.GET['userid']
	results = bookideal.objects.filter()
	datas = []
	for data in results:
		islike = 0
		buserid = data.userid
		if (len(concern.objects.filter(concernuser = userid,concerneduser = buserid))):
			if (len(like.objects.filter(userid = userid, bookidealid = data.id))):
				islike = 1
			datas.append({
				'idealid'  : data.id,
				'username' : data.username,
				'userhead' : data.userhead,
				'time'     : data.time,
				'content'  : data.content,
				'quote'    : data.quote,
				'likecount': data.likecount,
				'islike'   : islike
				})
	datas.reverse()
	return HttpResponse(json.dumps(datas),content_type="application/json")

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
		userhead = usermsg.userhead
		comment.objects.create(userid = userid, 
							   userhead = userhead,
							   username = username,
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
			data.append({
					"userid"   : re.userid, 
				    "userhead" : re.userhead,
				    "username" : re.username,
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
				    "userhead" : usermsg.userhead,
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
				    "userhead" : usermsg.userhead,
				    "signature": usermsg.signature,
				    "isconcern": isconcern
 				})
			data.reverse()
		return HttpResponse(json.dumps({'result':1,"data":data}),content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'result':0}),content_type="application/json")


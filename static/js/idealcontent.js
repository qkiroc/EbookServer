var userid = javaToJS.getUserid();
var bookidealid = javaToJS.getIdealid();
$(".content-top-user-time").append(format(time));
var isconcernflag = false;
var islike = false;
getcomment();
if(userid != idealuserid) {
	$.ajax({
		url: '/isconcern',
		type: 'post',
		dataType: 'json',
		data: {
			userid: userid,
			concerneduserid: idealuserid
		},
		success: data=>{
			if(data.result == 1){
				var concerndiv = `<div class="content-top-concern content-top-hasconcern"}></div>`
				isconcernflag = true;
			}
			else {
				var concerndiv = `<div class="content-top-concern content-top-notconcern"}></div>`
			}
			$(".content-top").append(concerndiv);
		}
	})
}
$.ajax({
	url: '/islike',
	type: 'post',
	dataType: 'json',
	data: {
		userid: userid,
		bookidealid: bookidealid
	},
	success: data=>{
		if(data.result == 1){
			$(".like").addClass('like-active');
			islike = true;
		}
	}
})
$(".like").click(function(event) {
	if(islike){
		$.ajax({
			url: '/notlike',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				idealid: bookidealid
			},
			success: (data)=>{
				if(data.result == 1) {
					$(this).removeClass('like-active');
					$(".likecount").html(parseInt($(".likecount").html())-1);
					islike=false;
				}
				else {
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
	}
	else {
		$.ajax({
			url: '/like',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				idealid: bookidealid
			},
			success: (data)=>{
				if(data.result == 1){
					$(this).children('i').css("transform", "scale(1.5)")
					setTimeout(()=>{
						$(this).children('i').css("transform", "scale(1)")
					}, 200)
					$(this).addClass('like-active')
					islike= true;

					$(".likecount").html(parseInt($(".likecount").html())+1);
				}
				else{
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
	}
});

$(document).on("click", ".content .content-top-concern", function(event) {
	if(isconcernflag){
		$.ajax({
			url: '/notconcern',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				concernedid: idealuserid
			},
			success: (data)=>{
				if(data.result == 1){
					$(this).removeClass("content-top-hasconcern")
					       .addClass('content-top-notconcern')
					isconcernflag = true;
				}
				else{
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
		isconcernflag = false;
	}
	else {
		$.ajax({
			url: '/concern',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				concernedid: idealuserid
			},
			success: (data)=>{
				if(data.result == 1){
					$(this).removeClass("content-top-notconcern")
					       .addClass('content-top-hasconcern')
					isconcernflag = true;
				}
				else{
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
	}
});

$(".share").click(function(event) {
	$.ajax({
		url: '/publish',
		type: 'post',
		dataType: 'json',
		data: {
			userid: userid,
			content: "(转发)"+$(".content-user-word").html(),
			quote: $(".content-original-word").html()
		},
		success:data=>{
			if(data.result == 1){
				javaToJS.showToast("分享成功");
			}
			else {
				javaToJS.showToast("失败，请稍后再试！");
			}
		}
	})
});

$(".coment").click(function(event) {
	$(".comenteditbg").fadeIn(10);
	$(".comentedit-textarea").focus().val();
});
$(".comenteditbg").click(function(event) {
	$(this).fadeOut(10);
});
$(".comentedit").click(function(event) {
	return false;
});
$(".comentbt").click(function(event) {
	var coment = $(".comentedit-textarea").val();
	if(coment){
		$.ajax({
			url: '/publishcomment',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				bookidealid: bookidealid,
				coment: coment
			},
			success:data=>{
				if(data.result == 1){
					getcomment();
					$('html,body').animate({scrollTop: document.body.clientHeight + 'px'},800);
					$(".comenteditbg").fadeOut(10);
				}
				else {
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
	
		
	}
	else {
		//TODO
	}
});
function getcomment(){
	$.ajax({
	url: '/getcomment',
	type: 'get',
	dataType: 'json',
	data: {
		bookidealid: bookidealid
	},
	success: re=>{
		if(re.result == 1){
			var comments = $("#comments");
			comments.children().remove();
			var j = 0;
			re.data.forEach((data,i)=>{
				j++;
				var comment = `<div class="comment">
									<div class="comment-user">
										<div class="comment-userhead" style={background:${data.userhead}}>
										</div>
										<div class="comment-username">${data.username}</div>
									</div>
									<div class="comment-word">${data.coment}</div>
									<div class="comment-time">${format(data.time)}</div>
								</div>`
				comments.append(comment);
			})
			$(".coments-count").html(j);
		}
		else {
			
		}
	}
})
}




function add0(m){return m<10?'0'+m:m }
function format(timestamp)
{	
	var time = new Date(parseInt(timestamp));
	var y = time.getFullYear();
	var m = time.getMonth()+1;
	var d = time.getDate();
	var h = time.getHours();
	var mm = time.getMinutes();
	var s = time.getSeconds();
	return y+'-'+add0(m)+'-'+add0(d);
}

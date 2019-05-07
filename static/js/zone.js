var userid = javaToJS.getUserid();
var type = javaToJS.getType();
$(document).on("click", "#con-find .like", function (e){
	if($(this).attr("data-flag") == "0") {
		$.ajax({
			url: '/like',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				idealid: $(this).attr('data-id')
			},
			success: (data)=>{
				if(data.result == 1){
					$(this).children('i').css("transform", "scale(1.5)")
					setTimeout(()=>{
						$(this).children('i').css("transform", "scale(1)")
					}, 200)
					$(this).addClass('like-active')
					       .attr('data-flag', '1');
					$(this).children('.likecount').html(parseInt($(this).children('.likecount').html())+1)
				}
				else{
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
		
		
	}
	else {
		$.ajax({
			url: '/notlike',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				idealid: $(this).attr('data-id')
			},
			success: (data)=>{
				if(data.result == 1) {
					$(this).removeClass('like-active')
		       			   .attr('data-flag', '0');
		       		$(this).children('.likecount').html(parseInt($(this).children('.likecount').html())-1)
				}
				else {
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})
		
		
	}
});

$(document).on("click", "#con-find .content-top-concern", function (e){
	if($(this).attr("data-flag") == "0") {
		$.ajax({
			url: '/concern',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				concernedid: $(this).attr('data-userid')
			},
			success: (data)=>{
				if(data.result == 1){
					$(this).removeClass("content-top-notconcern")
					       .addClass('content-top-hasconcern')
					       .attr('data-flag', '1');
				}
				else{
					javaToJS.showToast("失败，请稍后再试！");
				}
			}
		})	
	}
});
$(document).on("click", "#con-find .content-word", function(){
	var id = $(this).attr("data-id");
	javaToJS.toContent(id);
})
$(document).on("click", "#con-find .coment",function(){
	var id = $(this).attr("data-id");
	javaToJS.toContent(id);
})
$(document).on("click", "#con-find .share", function(){
	$.ajax({
		url: '/publish',
		type: 'post',
		dataType: 'json',
		data: {
			userid: userid,
			content: "(转发)"+$(this).children('.sharecontent').html(),
			quote: $(this).children('.sharequote').html()
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
})
var $conFind = $("#con-find");
$.ajax({
	url: '/get'+type+'bookideal',
	type: 'get',
	dataType: 'json',
	data: {userid: userid},
	success: function(result) {
		result.forEach(function(data,i){
			var content =`
			<div class="content">
				<div class="content-top">
					<div class="content-top-user">
						<div class="content-top-user-head" style={background:${data.userhead}}>
						</div>
						<div class="content-top-user-name">${data.username}</div>
						<div class="content-top-user-time">${format(data.time)}</div>
					</div>
					<div data-flag=${data.isconcern} 
						 data-userid=${data.userid}
						 style=display:${data.userid == userid||type=="concern"?"none":"block"} 
						 class="content-top-concern ${!data.isconcern?"content-top-notconcern":"content-top-hasconcern"}"></div>
				</div>
				<div class="content-word" data-id=${data.idealid}>
					<div class="content-user-word">
						${data.content}
					</div>
					<div class="content-original-word">
						<span>${data.quote}</span>
					</div>
				</div>
				<div class="content-footer">
					<div class="share">
						<div class="sharecontent" style ="display:none">${data.content}</div>
						<div class="sharequote" style ="display:none">${data.quote}</div>
						<i class="iconfont icon-fenxiang"></i>
						<span>分享</span>
					</div>
					<div class="coment" data-id=${data.idealid}>
						<i class="iconfont icon-pinglun"></i>
						<span>评论</span>
					</div>
					<div data-id=${data.idealid} class="like ${data.islike?"like-active":""}" data-flag=${data.islike}>
						<i class="iconfont icon-dianzan"></i>
						<span class="likecount">${data.likecount}</span>
					</div>
				</div>
			</div>
			`
			$conFind.append(content);
		})
	}
})
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


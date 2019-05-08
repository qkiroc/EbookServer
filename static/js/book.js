$("#goback").click(function(event) {
	javaToJS.filishActive();
});
var userid = javaToJS.getUserid();
var bookid = window.location.href.split("=")[1];
var iswant = false;
getcomment();
$.ajax({
	url: '/isbooklike',
	type: 'post',
	dataType: 'json',
	data: {
		userid: userid,
		bookid: bookid
	},
	success: data=>{
		if (data.result == 1){
			$(".want").children('i').removeClass('icon-aixin')
				      .addClass('icon-aixin_shixin')
					  .css('color', '#FF9800');
			iswant = true;
		}
	}
})
$(".want").click(function(event) {
	if(userid){
		if(!iswant) {
			$.ajax({
				url: '/postbooklike',
				type: 'post',
				dataType: 'json',
				data: {
					userid: userid,
					bookid: bookid
				},
				success: data=>{
					if (data.result == 1) {
						$(this).children('i').removeClass('icon-aixin')
						       .addClass('icon-aixin_shixin')
							   .css('color', '#FF9800');
						iswant = true;
					}else {
						javaToJS.showToast("请求错误，请稍后重试");
					}
				}
			})
			
			
		}
		else {
			$.ajax({
				url: '/postbooknotlike',
				type: 'post',
				dataType: 'json',
				data: {
					userid: userid,
					bookid: bookid
				},
				success: data=>{
					if (data.result == 1) {
						$(this).children('i').addClass('icon-aixin')
							   .removeClass('icon-aixin_shixin')
							   .css('color', '#828282');
						iswant = false;
					}else {
						javaToJS.showToast("请求错误，请稍后重试");
					}
				}
			})
			
		}
	}
	else {
		javaToJS.showToast("请先登录");
	}
	
});
$(".commend").click(function(event) {
	if(userid){
		$(".comenteditbg").fadeIn(10);
		$(".comentedit-textarea").focus().val();
	}
	else {
		javaToJS.showToast("请先登录");
	}
	
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
			url: '/publishbookcomment',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				bookid: bookid,
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
		url: '/getbookcomment',
		type: 'get',
		dataType: 'json',
		data: {
			bookid: bookid
		},
		success: re=>{
			if(re.result == 1){
				var comments = $(".coment-content");
				comments.children().remove();
				var j = 0;
				re.data.forEach((data,i)=>{
					j++;
					var comment = `<div class="coment-content-in">
										<div class="user">
											<div class="user-head" style={background:${data.userhead}>
												
											</div>
											<div class="user-name">
												${data.username}
											</div>
										</div>
										<div class="coment-content-in-word">
											${data.coment}
										</div>
										<div class="time">
											${format(data.time)}
										</div>
									</div>`
					comments.append(comment);
				});
				if (j == 0){
					comments.html(`<div class="contentword">暂时还没有内容...</div>`);
				}
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
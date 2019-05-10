var userid = javaToJS.getUserid();
var type = parseInt(window.location.href.split("=")[1]);
var content = $('.content');
var loading = $(".loading");
var page = 1;
var flag = true;
var iscomplete = true;
if (type != 10) {
	$(".banner").hide();
}
switch (type) {
	case 0:
		type = "玄幻奇幻"
		break;
	case 1:
		type = "武侠仙侠"
		break;
	case 2:
		type = "女频言情"
		break;
	case 3:
		type = "现代都市"
		break;
	case 4:
		type = "历史军事"
		break;
	case 5:
		type = "游戏竞技"
		break;
	case 6:
		type = "科幻灵异"
		break;
	case 7:
		type = "美文同人"
		break;
	case 8:
		type = "剧本教程"
		break;
	case 9:
		type = "名著杂志"
		break;
	case 10:
		type = "all"
		break;
}
getContent(page,type);
function getContent(p, type) {
	$.ajax({
		url: '/getbooks',
		type: 'get',
		dataType: 'json',
		data: {
			userid: userid,
			page: p,
			type: type
		},
		beforeSend: function(){
			loading.show();
			iscomplete = false;
		},
		complete: function(){
			loading.hide();
			iscomplete = true;
		},
		success: re=>{
			if(re.result == 1) {
				if (re.data.length > 0) {
					re.data.forEach((data, i)=>{
						var book = `
							<div class="book" data-id=${data.id}>
								<div class="pic">
									<img src="/static/bookcover/${data.title}.jpg" alt="">
								</div>
								<div class="word">
									<div class="title">${data.title}</div>
									<div class="brief">${data.brief}</div>
									<div class="author">${data.author}</div>
								</div>
							</div>
						`
						content.append(book)
					})
					page ++;
				}
				else {
					content.html(`<div class="contentword">暂时还没有内容...</div>`)
				}
				
			}
			else if(re.result == 2){
				$(".over").show();
				flag = false;
			}
			else {
				javaToJS.showToast("请求错误，请稍后再试");
			}
		}
	})	
}
function loadcontent(){
	if (flag && iscomplete){
		getContent(page, type);
	}
}
$(document).on("click", ".content .book",function(){
	javaToJS.toContent($(this).attr('data-id'));
})
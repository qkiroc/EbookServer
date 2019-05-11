var userid = javaToJS.getUserid();
var page = 1;
var flag = true;
var iscomplete = true;
getcontent(page);
function getcontent(p) {
	$.ajax({
		url: '/getwantread',
		type: 'get',
		dataType: 'json',
		data: {
			userid: userid,
			page: p
		},
		beforeSend: function(){
			$(".loading").show();
			iscomplete = false;
		},
		complete: function(){
			$(".loading").hide();
			iscomplete = true;
		},
		success: re=>{
			if(re.result == 1){
				var wantread = $(".wantread");
				if(re.data.length > 0){
					re.data.forEach( (data, i)=> {
						var content = `<div class="book" data-id=${data.id}>
											<div class="delete" data-id=${data.id}>
												<i class="iconfont icon-shanchu"></i>
											</div>
											<div class="pic">
												<img src="/static/bookcover/${data.title}.jpg" alt="">
											</div>
											<div class="word">
												<div class="title">${data.title}</div>
												<div class="brief">${data.brief}</div>
												<div class="author">${data.author}</div>
											</div>
										</div>`
						wantread.append(content);
					});
					
					page++;
				}
				else {
					wantread.html("<div class='contentword'>暂时还没有内容...<div>")
				}

			}
			else if (re.result == 2) {
				$(".over").show();
				flag = false;
			}
			else {
				javaToJS.showToast("请求错误，请稍后再试");
			}
		}
	})
}
$(document).on("click", ".wantread .delete", function(){
	$.ajax({
		url: '/postbooknotlike',
		type: 'post',
		dataType: 'json',
		data: {
			userid: userid,
			bookid: $(this).attr('data-id')
		},
		success: data=>{
			if(data.result == 1){
				$(this).parent().remove();
			}
			else {
				javaToJS.showToast("请求错误，请稍后再试");
			}
		}
	})
	return false;
})
$(document).on("click", ".wantread .book", function(){
	javaToJS.toContent($(this).attr('data-id'));
})
function loadcontent() {
	if (flag && iscomplete){
		getcontent(page);
	}
}
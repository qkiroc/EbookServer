var loading = $(".loading");
var content = $(".content");
var page = 1;
var flag = true;
var iscomplete = true;
var keyword = "";
function getcontent(p,keyword){
	$.ajax({
		url: '/getbooksearch',
		type: 'get',
		dataType: 'json',
		data: {
			page: p,
			keyword: keyword
		},
		beforeSend: function(){
			loading.show();
			iscomplete = false;
		},
		complete: function(data){
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
		getcontent(page, keyword);
	}
}
function search(key) {
	page = 1;
	keyword = key
	content.children().remove()
	getcontent(1, keyword);
}
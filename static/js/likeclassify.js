var userid = javaToJS.getUserid();
var flag = true;
var items = new Set();
$.ajax({
	url: '/getlikeclassify',
	type: 'get',
	dataType: 'json',
	data: {
		userid:userid
	},
	success: re=>{
		if(re.result == 1){
			var mine = $(".mine-content");
			re.data.forEach((data,i)=>{
				items.add(data)
				mine.append(`<div class="item">${data}</div>`)
			})
		}
		else {
			javaToJS.showToast("请求错误，请稍后再试");
		}
	}
})
$(".button").click(function(event) {
	if (flag){
		$(this).html("完成");
		$(".mine .item").addClass('mine-item');
		$(".classify .item").addClass('classify-item');
		flag = false;
	}
	else {
		$(this).html("编辑");
		$(".mine .item").removeClass('mine-item');
		$(".classify .item").removeClass('classify-item');
		console.log(items);
		$.ajax({
			url: '/postlikeclassify',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				items: Array.from(items).join(","),
			},
			success: data=>{

			}
		})
		
		flag = true;
	}
});
$(document).on("click", ".mine .item", function(){
	if(!flag){
		$(this).remove();
		items.delete($(this).html());
	}
	
});
$(document).on("click", ".classify .item", function(){
	if(!flag){
		if (!items.has($(this).html())){
			var item = $(this).clone().removeClass('classify-item').addClass('mine-item');
			items.add($(this).html());
			$(".mine-content").append(item);
		}
		
	}
})
$(".goback").click(function(event) {
	javaToJS.finishActive()
});
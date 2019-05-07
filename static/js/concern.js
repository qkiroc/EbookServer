var userid = javaToJS.getUserid();
var type = javaToJS.getType();
var main = $(".main");
$.ajax({
	url: '/get'+type,
	type: 'get',
	dataType: 'json',
	data: {
		userid: userid
	},
	success: re=>{
		if (re.result == 1) {
			re.data.forEach((data,i)=>{
				var content = `
						<div class="content">
							<div class="userhead" style="background:${data.userhead}"></div>
							<div class="nameandsignature">
								<div class="username">${data.username}</div>
								<div class="signature">${data.signature}</div>
							</div>
							<div class="concern ${data.isconcern?"hasconcern":"notconcern"}" data-id=${data.userid} data-flag=${data.isconcern}>
								
							</div>`
				main.append(content);

			})
		}
	}
})
$(document).on("click", ".main .concern", function(){
	if($(this).attr("data-flag") == 1){
		$.ajax({
			url: '/notconcern',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				concernedid: $(this).attr('data-id')
			},
			success:data=>{
				if(data.result == 1){
					$(this).removeClass('hasconcern')
				       .addClass('notconcern')
				       .attr('data-flag', 0);
				}
				else {
					
				}
				
			}
		})	
	}
	else {
		$.ajax({
			url: '/concern',
			type: 'post',
			dataType: 'json',
			data: {
				userid: userid,
				concernedid: $(this).attr('data-id')
			},
			success:data=>{
				if(data.result == 1){
					$(this).removeClass('notconcern')
					       .addClass('hasconcern')
					       .attr('data-flag', 1);
				}
				else {
					
				}
				
			}
		})
	}
	
})

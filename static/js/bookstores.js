var con = $("#con");
var con_in = $("#con_in");
var bt_recommend = $("#bt_recommend");
var bt_novel = $("#bt_novel");
var bt_masterwork = $("#bt_masterwork");
var bt_magazine = $("#bt_magazine");
var flag = 1;
con.on("swipeleft", function(e){
	if (flag == 3) {
		con_in.css("transform","translateX(-15rem)");
		bt_masterwork.removeClass('nav-active');
		bt_magazine.addClass('nav-active');
		flag = 4;
	}
	if (flag == 2) {
		con_in.css("transform","translateX(-10rem)");
		bt_novel.removeClass('nav-active');
		bt_masterwork.addClass('nav-active');
		flag = 3;
	}
	if (flag == 1) {
		con_in.css("transform","translateX(-5rem)");
		bt_recommend.removeClass('nav-active');
		bt_novel.addClass('nav-active');
		flag = 2;
	}
})
con.on("swiperight", function(e){
	if (flag == 2) {
		con_in.css("transform","translateX(0rem)");
		bt_novel.removeClass('nav-active');
		bt_recommend.addClass('nav-active');
		flag = 1;
	}
	if (flag == 3) {
		con_in.css("transform","translateX(-5rem)");
		bt_masterwork.removeClass('nav-active');
		bt_novel.addClass('nav-active');
		flag = 2;
	}
	if (flag == 4) {
		con_in.css("transform","translateX(-10rem)");
		bt_magazine.removeClass('nav-active');
		bt_masterwork.addClass('nav-active');
		flag = 3;
	}
})
bt_recommend.on("tap", function(){
	con_in.css("transform","translateX(0rem)");
	bt_recommend.siblings().removeClass('nav-active');
	bt_recommend.addClass('nav-active');
	flag = 1;
})
bt_novel.on("tap", function(){
	con_in.css("transform","translateX(-5rem)");
	bt_novel.siblings().removeClass('nav-active');
	bt_novel.addClass('nav-active');
	flag = 2;
})
bt_masterwork.on("tap", function(){
	con_in.css("transform","translateX(-10rem)");
	bt_masterwork.siblings().removeClass('nav-active');
	bt_masterwork.addClass('nav-active');
	flag = 3;
})
bt_magazine.on("tap", function(){
	con_in.css("transform","translateX(-15rem)");
	bt_magazine.siblings().removeClass('nav-active');
	bt_magazine.addClass('nav-active');
	flag = 4;
})
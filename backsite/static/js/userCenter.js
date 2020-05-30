function pageInit(){
	document.body.style.backgroundImage = "url(/static/img/BG.png)";
	
	userCenter_checkLogin();
	
	topNavInit();
	
	titleInit();
	
	setUserData(1);
	
	bindKeyPress();
	
	initSwitchBtn();
}

// 更改网页title
function titleInit(){
	var nickname = '我';
	$.ajax({
		url:'/api/user/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		async: false,//同步的方式,获取结果在继续下面的步骤
		data: {
			'what': 'nickname',
			'token': getToken(),
		},// data是必须的,可以空,不能没有
		success:function(ret){
			if (ret.code == '200'){
				nickname = ret.data;
			}
			else if(ret.code=='403'){
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error:function(xhr,type,errorThrown){
			//console.log(errorThrown);
		}
	});
	if (nickname.length>=6){
		nickname = nickname.slice(0,5)+'...';
	}
	document.title = "Compayu | " + nickname + "的个人空间";
}


// 填入用户现在的信息
function setUserData(page){
	// 头像
	var avatar = document.getElementById("userCenter_avatar");
	$.ajax({
		url:'/api/user/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
			'what' : 'avatar',
		},// data是必须的,可以空,不能没有
		success:function(ret){
			if (ret.code == '200' && ret.data != 'https://cdn.wzz.ink/avatar/defaultAvatar.png'){
				avatar.setAttribute('src', ret.data);
			}
			else if(ret.code=='403'){
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error:function(xhr,type,errorThrown){
			console.log(errorThrown);
		}
	});
	// user
	var userinfo;
	$.ajax({
		url:'/api/user/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		async: false,
		data: {
			'token': getToken(),
			'what' : 'userinfo',
		},// data是必须的,可以空,不能没有
		success:function(ret){
			if (ret.code == '200'){
				userinfo = ret;
			}
			else if(ret.code=='403'){
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error:function(xhr,type,errorThrown){
			console.log(errorThrown);
		}
	});
	document.getElementById("userType").innerHTML = userinfo.usertype;
	document.getElementById("userLevel").innerHTML = "LV"+parseInt(userinfo.level/100);
	document.getElementById("userCenter_nickname").innerHTML = userinfo.nickname;
	document.getElementById("userCenter_signature").value = userinfo.signature;
	if (userinfo.email){
		var email = document.getElementById("userCenter_up_email");
		email.setAttribute('src', "/static/img/email_on.png");
	}
	if (userinfo.phone){
		var phone = document.getElementById("userCenter_up_phone");
		phone.setAttribute('src', "/static/img/phone_on.png");
	}
	// 按页码填充数据
	if (page == 1){
		// 个人主页
		
	}
}

//上传头像
function changeAvatar(){
	var input = document.getElementById("avatar_input");
	input.click();
	var fileReader = new FileReader();
	$('#avatar_input').change(function () {
		var obj = $(this)[0].files[0];
		fileReader.readAsDataURL(obj);
		//等待读取完毕后，将文件加载到img标签中
		fileReader.onload = function () {
			// 先上传,再前端显示
			uploadAvatar();
			$('#userCenter_avatar').attr('src',fileReader.result)
		}
	})
}

function uploadAvatar(){
	var formdata = new FormData();
	formdata.append("avatar", $("#avatar_input")[0].files[0]);
	formdata.append('token',getToken());
	$.ajax({
		processData:false,
		contentType:false,
		url:'/api/avatar/',
		type:'post',
		data:formdata,
		dataType:"json",
		success:function (arg) {
			if (ret.code == '200'){
				userinfo = ret;
			}
			else if(ret.code=='403'){
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},error: function () {
			//alert("访问繁忙，请重试")
		}

	})
}

//上传新的签名
function changeSignature(sig){
	$.ajax({
		url:'/api/user/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
			'what' : 'setuser',
			'where' : 'signature',
			'data' : sig,
		},// data是必须的,可以空,不能没有
		success:function(ret){
			if (ret.code == '200' ){
				alert('修改成功');
			}
			else if(ret.code=='403'){
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error:function(xhr,type,errorThrown){
			console.log(errorThrown);
		}
	});
}

// 绑定按键输入
function bindKeyPress(){
	$('#userCenter_signature').bind('keydown',function(event){
		if(event.keyCode == "13") {
	        var sig = document.getElementById("userCenter_signature");
			changeSignature(sig.value);
	    }
	});
}

function logout(){
	$.ajax({
		url:'/user/logout/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
		},// data是必须的,可以空,不能没有
		success:function(ret){
			jumpToIndex();
		},
		error:function(xhr,type,errorThrown){
			console.log(errorThrown);
		}
	});
}

function initSwitchBtn(){
	var btns_p = document.getElementsByClassName("userCenter_btn_p");
	var page = 0;
	if (which=='myinfo'){
		// 第一页
		page = 0;
	}else if(which=='mymessage'){
		page = 1;
	}else if(which=='mysafety'){
		page = 2;
	}else if(which=='mynews'){
		page = 3;
	}else if(which=='mystar'){
		page = 4;
	}
	
	for (var i=0;i<btns_p.length;i++){
		if (i==page){
			btns_p[i].style.color = '#4169E1';
		}else{
			btns_p[i].style.color = "black";
		}
	}
	// 滑块
	var subline = document.getElementById("userCenter_subline");
	var left = 10 + (10 + 160) * page;
	subline.style.marginLeft = left+'px';
}

function userCenter_checkLogin(){
	var isLogin = checkLogin();
	if (isLogin == "False"){
		alert("您的账号状态异常,请重新登录");
		jumpToLogin();
	}
}

function switchBtn_hover(w){
	if (w==0){
		//归位
		initSwitchBtn();
	}else{
		var btns_p = document.getElementsByClassName("userCenter_btn_p");
		btns_p[w-1].style.color = '#4169E1';
		// 滑块
		var subline = document.getElementById("userCenter_subline");
		var left = 10 + (10 + 160) * (w-1);
		subline.style.marginLeft = left+'px';
	}
}

function userCenter_changePage(p){
	if (p==1){
		window.location.href = '/user/usercenter/?which=myinfo';
	}else if(p==2){
		window.location.href = '/user/usercenter/?which=mymessage';
	}else if(p==3){
		window.location.href = '/user/usercenter/?which=mysafety';
	}else if(p==4){
		window.location.href = '/user/usercenter/?which=mynews';
	}else if(p==5){
		window.location.href = '/user/usercenter/?which=mystar';
	}
}
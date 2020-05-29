
// 返回门户页面
function jumpToIndex(){
	window.location.href = '/';
}

//关于我们
function jumpToAboutUs(){
	window.open('/website');
}
//用户中心
function jumpToUsercenter(){
	window.location.href = '/user/usercenter';
}

//跳转到登录界面
function jumpToLogin(){
	window.location.href = '/user/?type=login';
}

//跳转到注册界面
function jumpToRegister(){
	window.location.href = '/user/?type=register';
}

//忘记密码的处理
function jumpToForgetPassword(){
	
}

//打开用户管理小列表
function openUserList(){
	window.open('/user/usercenter/?which=myinfo');
}

//-----------顶部导航栏的处理代码也放在这里--------------
function topNavInit(){
	initShowNav();
		
	checkLogin();
}


function initShowNav(){
	slide = document.getElementById("topNav_slider");
	slide.style.marginTop = 0;
	setTimeout(function(){
		slide.style.marginTop = -80 + 'px';
		slide.style.background = 'transparent';
	},1500);
}

function topNavSlide(w){
	slide = document.getElementById("topNav_slider");
	if (w == 1){
		slide.style.marginTop = '0';
	}else if(w==2){
		slide.style.marginTop = -80 + 'px';
	}
}

function checkLogin(){
	// 检查islogin 的cookie判断是否登录
	var isLogin = checkAcStatus();
	
	var p1 = document.getElementById("topNav_RegisterOrLogin");
	var p2 = document.getElementById("userinfoContainer");
	//console.log(isLogin);
	if (isLogin == "True"){
		p2.style.display = "flex";
		p1.style.display = "none";
		// 改头像和昵称
		var nickname = document.getElementById("topNav_nickname");
		$.ajax({
			url:'/api/user/',
			type:'POST',//HTTP请求类型
			timeout:5000,//超时时间设置为10秒；
			dataType: "json",
			data: {
				'what': 'nickname',
				'token': getToken(),
			},// data是必须的,可以空,不能没有
			success:function(ret){
				if (ret.code == '200'){
					nickname.innerHTML = ret.data;
					setCookie("nickname", nickname.innerHTML);
					nickname.setAttribute('title', nickname.innerHTML);
					//console.log(nickname.innerHTML);
					if (nickname.innerHTML.length >= 6){
						nickname.innerHTML = nickname.innerHTML.slice(0,5) + '...';
					}
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
		var avatar = document.getElementById("topNav_avatar");
		//console.log(getToken());
		var api = {'token': getToken(), "what": 'avatar'};
		$.ajax({
			url:'/api/user/',
			type:'POST',//HTTP请求类型
			timeout:5000,//超时时间设置为10秒；
			dataType: "json",
			data: api,// data是必须的,可以空,不能没有
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
	}else{
		p1.style.display = "flex";
		p2.style.display = "none";
	}
}

function saveToken(token){
	window.localStorage.setItem('token', token);
	// 跳转到主页
	//window.location.href = '/';
}

function setCookie(name, value) { 
	var exp = new Date(); 
	// 自动登录时间
	var time;
	$.ajax({
		url:'/api/settings/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为10秒；
		dataType: "json",
		data: {
			'what': 'logintime',
		},// data是必须的,可以空,不能没有
		success:function(ret){
			time = ret.data;
		},
		error:function(xhr,type,errorThrown){
			time = 60 * 30 * 1000;
		}
	});
	//console.log(time);
	exp.setTime(exp.getTime() + time); 
	document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/"; 
} 

//读取cookies 
function getCookie(name) { 
	var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)"); 
	var ret = null;
	if (arr = document.cookie.match(reg)){ 
		ret = unescape(arr[2]); 
	}else{ 
		ret = null; 
	}
	// 因为如果储存的ID是邮箱,那么会自动带有引号,需要判断后去掉
	if (ret[0].charCodeAt() == 34){
		ret = ret.slice(1,ret.length-1);
	};
	return ret;
} 

function getToken(){
    var data = localStorage.getItem('token');
	if (data){
		return data;
	}
	return '';
}

// 通过token检查用户登录状态
function checkAcStatus(){
	var isLogin = 'False';
	// 调用api检查登录是否过期
	$.ajax({
		url:'/api/token/',
		type:'POST',//HTTP请求类型
		timeout:5000,//超时时间设置为5秒；
		dataType: "json",
		async: false,//同步的方式,获取结果在继续下面的步骤
		data:{
			'token' : getToken(),
		},// data是必须的,可以空,不能没有
		success:function(ret){
			isLogin = ret.data;
			console.log("Account status: is Login? "+ isLogin);
		},
		error:function(xhr,type,errorThrown){
			console.log(errorThrown);
		}
	});
	return isLogin;
}

function pageInit(){
	document.body.style.backgroundImage = "url(/static/img/BG.png)";
	
	topNavInit();
	
	welcome();
	
	// 子表单的处理总应该先于他的父表单
	initRegisterType();
	
	changeByType();
	
	// 如果有上次记住密码的功能,自动填充表格
	checkAutoLogin();
}

// vue
var data_btn1 = { userBtn1: "获取验证码" }
var vm_btn1 = new Vue({
	el: '#getValidcodeBtn',
	data: data_btn1,
})
var data_btn2 = { userBtn2: "发送邮件" }
var vm_btn2 = new Vue({
	el: '#getValidcodeBtn2',
	data: data_btn2,
})


function welcome(){
	var p1 = document.getElementById("user_welcome_p1");
	var p2 = document.getElementById("user_welcome_p2");
	var func = document.getElementById("functionContainer");
	var wel = document.getElementById("user_welcome");
	var icon = document.getElementById("user_bigIcon");
	setTimeout(function(){
		p1.style.opacity = 1;
		p2.style.opacity = 1;
		setTimeout(function(){
			p1.style.transform = "perspective(1500px) rotateX(-30deg)";
			p2.style.transform = "perspective(1500px) rotateX(-30deg)";
			setTimeout(function(){
				p1.style.marginTop = -50+'px';
				//p2.style.marginTop = -50+'px';
				p1.style.opacity = 0;
				p2.style.opacity = 0;
				setTimeout(function(){
					wel.style.display = "none";
					icon.style.display = 'flex';
					setTimeout(function(){
						func.style.display = "flex";
						func.style.opacity = "1";
						icon.style.opacity = "1";
					},500);
				},300);
			},100);
		},1500);
	},500);
}

function changeByType(){
	var btn1 = document.getElementById("user_loginBtn");
	var btn2 = document.getElementById("user_registerBtn");
	//console.log(type);
	if (type == 'register'){
		//显示注册页
		btn2.style.background = "#4169E1";
		btn2.style.color = 'white';
		switchPage(2);
	}
	else if(type == 'login'){
		//显示登陆页
		btn1.style.background = "#4169E1";
		btn1.style.color = 'white';
		switchPage(1);
	}
}

function switchPage(w){
	var b1 = document.getElementById("user_loginBtn");
	var b2 = document.getElementById("user_registerBtn");
	var container = document.getElementById("functionContainer");
	var userslider = document.getElementById("user_subPageSlider");
	
	if (w==2){
		container.style.height = "450px";
		userslider.style.marginLeft = "-100%";
		b2.style.background = '#4169E1';
		b1.style.background = '#F8F8FF';
		b2.style.color = 'white';
		b1.style.color = 'black';
	}else if (w==1){
		container.style.height = "370px";
		userslider.style.marginLeft = "0";
		b1.style.background = '#4169E1';
		b2.style.background = '#F8F8FF';
		b1.style.color = 'white';
		b2.style.color = 'black';
	}
}

//检查通过账号登录的规范性
function loginCheck(){
	var uac = document.getElementById("UserLogin_form_ac");
	var upw = document.getElementById("UserLogin_form_pw");
	if (uac.value == ''){
		uac.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入电话或邮箱号");
		return;
	}
	if (upw.value == ''){
		upw.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入您的密码");
		return;
	}
	var rememAc = document.getElementsByName('rememAC')[0];
	// checkbox的值不是tm的value,是.checked
	// md5
	var retpwd = '';
	if (getCookie('uac') == null || getCookie('uac') != uac.value){
		// 如果是新输入的密码就需要加密
		// 1.储存的密码过期了 2.用户新输入了一个账号
		retpwd = md5(upw.value);
	}else{
		retpwd = getCookie('upw');
	}
	
	var user = { "uac" : uac.value, "upw" : retpwd, "rememAc" : rememAc.checked };
	$.ajax({
		url:'/user/login/',
		data:JSON.stringify(user),
		type:'post',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		async: false,//同步的方式
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		success:function(data){
			if (data.msg == "用户名或密码错误"){
				alert(data.msg);
				uac.style.borderBottom = "#FF2200 solid 2px";
				upw.style.borderBottom = "#FF2200 solid 2px";
			}
			else if(data.msg == "登入成功"){
				//在本地存储这个token
				//后续的api调用都需要在头文件中添加这个token
				saveToken(data.token);
				//更新顶部导航栏
				//checkLogin();
				jumpToUsercenter();
				// jumpToIndex();
			}
		},
		error:function(xhr,type,errorThrown){
			alert("数据传输失败,请稍后重试");
		}
	});
}

//检查注册
// w=1 : phone ; w=2 : email ; w = 3 : othertype
function registerCheck(w){
	// 电话注册
	if (w==1){
		var form = document.getElementById("registerForm1");
		var phone = document.getElementById("phonenum");
		if (!checkPhone(phone.value)){
			phone.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入符合规范的电话号码");
			return;
		}
		var validcode = document.getElementById("validcode");
		if (validcode.value == ''){
			validcode.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入验证码");
			return;
		}
		var nickname = document.getElementById("nickname1");
		if (nickname.value == ''){
			nickname.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入您的昵称");
			return;
		}
		var pwd = document.getElementById("pw1");
		if (pwd.value == ''){
			pwd.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入密码");
			return;
		}
		form.submit();
	}
	//邮箱注册
	else if(w==2){
		var form2 = document.getElementById("registerForm2");
		var email = document.getElementById("email");
		if (!checkEmail(email.value)){
			email.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入符合规范的电子邮箱");
			return;
		}
		var validecode2 = document.getElementById("validcode2");
		if (validecode2.value.length <6){
			validecode2.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入邮件中的验证码");
			return;
		}
		var nickname2 = document.getElementById("nickname2");
		if (nickname2.value == ''){
			nickname2.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入您的昵称");
			return;
		}
		var pwd2 = document.getElementById("pw2");
		if (pwd2.value == ''){
			pwd2.style.borderBottom = "#FF2200 solid 2px";
			alert("请输入密码");
			return;
		}
		form2.submit();
	}
	
}

//检查是否可以发送验证码
function sendValidCode(){
	// 先检查这个号码是否规范
	var phone = document.getElementById("phonenum");
	var btn1 = document.getElementById("getValidcodeBtn");
	if (!checkPhone(phone.value)){
		phone.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入符合规范的电话号码");
		return;
	}
	// 让发送按钮失效
	data_btn1.userBtn1 = '发送中...';
	btn1.setAttribute("disabled","disabled");
	$.ajax({
		url:'/user/register/sendvalidcode',
		data:{
			"phone" : phone.value,
		},
		type:'post',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		async: false,//同步的方式
		success:function(data){
			alert(data);
			startTiming(1,btn1,60);
		},
		error:function(xhr,type,errorThrown){
			alert("操作失败,请稍后重试");
		}
	});
}

function sendEmailCode(){
	var email = document.getElementById("email");
	var btn2 = document.getElementById("getValidcodeBtn2");
	if (!checkEmail(email.value)){
		email.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入符合规范的电子邮箱");
		return;
	}
	// 让发送按钮失效
	data_btn2.userBtn2 = '发送中...';
	btn2.setAttribute("disabled","disabled");
	$.ajax({
		url:'/user/register/sendemail',
		data:{
			"email" : email.value,
		},
		type:'post',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		async: false,//同步的方式
		success:function(data){
			alert(data);
			startTiming(2,btn2,60);
		},
		error:function(xhr,type,errorThrown){
			alert("操作失败,请稍后重试");
		}
	});
}

function openOtherChannel(){
	var openBtn = document.getElementById("user_subPage1_other_open_p");
	var other = document.getElementById("user_subPage1_otherchannel");
	var container = document.getElementById("functionContainer");
	//console.log(openBtn.innerHTML);
	if (openBtn.innerHTML == "其他登录方式 &gt; "){
		openBtn.innerHTML = "关闭 < ";
		other.style.display = 'flex';
		container.style.height = "450px";
	}else {
		openBtn.innerHTML = "其他登录方式 > ";
		other.style.display = 'none';
		container.style.height = "370px";
	}
}

function initRegisterType(){
	var btn1 = document.getElementById("subPage2_phoneBtn"); 
	btn1.style.color = "#2244CC";
	switchRegister(1);
}

function switchRegister(w){
	var btn1 = document.getElementById("subPage2_phoneBtn");
	var btn2 = document.getElementById("subPage2_emailBtn"); 
	var btn3 = document.getElementById("subPage2_other"); 
	var subline = document.getElementById("user_subline");
	var slider = document.getElementById("user_subPage2_slider");
	var container = document.getElementById("functionContainer");
	if (w==1){
		btn1.style.color = "#2244CC";
		btn2.style.color = "black";
		btn3.style.color = 'black';
		subline.style.marginLeft = "4%";
		slider.style.marginLeft = '0%';
		container.style.height = "450px";
	}else if (w==2){
		btn2.style.color = "#2244CC";
		btn1.style.color = "black";
		btn3.style.color = 'black';
		subline.style.marginLeft = "36%";
		slider.style.marginLeft = '-100%';
		container.style.height = "430px";
	}else if (w==3){
		btn3.style.color = "#2244CC";
		btn2.style.color = "black";
		btn1.style.color = 'black';
		subline.style.marginLeft = "66%";
		slider.style.marginLeft = '-200%';
	}
}

function closeImediatly(){
	var p1 = document.getElementById("user_welcome_p1");
	var p2 = document.getElementById("user_welcome_p2");
	var func = document.getElementById("functionContainer");
	var wel = document.getElementById("user_welcome");
	var icon = document.getElementById("user_bigIcon");
	p1.style.transform = "perspective(1500px) rotateX(-30deg)";
	p2.style.transform = "perspective(1500px) rotateX(-30deg)";
	setTimeout(function(){
		p1.style.marginTop = -50+'px';
		//p2.style.marginTop = -50+'px';
		p1.style.opacity = 0;
		p2.style.opacity = 0;
		setTimeout(function(){
			wel.style.display = "none";
			icon.style.display = 'flex';
			setTimeout(function(){
				func.style.display = "flex";
				func.style.opacity = "1";
				icon.style.opacity = "1";
			},500);
		},300);
	},100);
}

// 判断输入的电话号码是否可用
function checkPhone(num){
	var strTemp = /^1[3|4|5|6|7|8|9][0-9]{9}$/;
	if (strTemp.test(num)){
		return true;
	}
	return false;
}

function checkEmail(email){
	var myReg=/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
	if(myReg.test(email)){
		return true;
	}
	return false;
}

function showReliable(w){
	var pw1 = document.getElementById("pw1");
	var pw2 = document.getElementById("pw2");
	var s1 = document.getElementById("showLs1");
	var s2 = document.getElementById("showLs2");
	var ls = 0;
	if (w==1){
		ls = getPwLs(pw1.value);
		s1.style.display = 'flex';
		if (pw1.value.length == 0){
			s1.style.display = 'none';
		}
	}else if(w==2){
		ls = getPwLs(pw2.value);
		s2.style.display = 'flex';
		if (pw2.value.length == 0){
			s2.style.display = 'none';
		}
	}
	if (w==1){
		var s1_1ist = [document.getElementById("showLs1_block1"),document.getElementById("showLs1_block2"),document.getElementById("showLs1_block3")];
		for (var t=0;t<s1_1ist.length;t++){
			s1_1ist[t].style.opacity = '0';
		}
		for (var t=0;t<ls;t++){
			s1_1ist[t].style.opacity = '1';
		}
	}else if (w==2){
		var s2_1ist = [document.getElementById("showLs2_block1"),document.getElementById("showLs2_block2"),document.getElementById("showLs2_block3")];
		for (var t=0;t<s2_1ist.length;t++){
			s2_1ist[t].style.opacity = '0';
		}
		for (var t=0;t<ls;t++){
			s2_1ist[t].style.opacity = '1';
		}
	}
}

// 注册密码复杂度
function getPwLs(s){ 
	var ls = 0;     
	
	if(s.match(/([a-z])+/)){     
		ls++;     
	}     	
	if(s.match(/([0-9])+/)){     
		ls++;       
	}     	
	if(s.match(/([A-Z])+/)){     
		ls++;     
	}     
	if(s.match(/[^a-zA-Z0-9]+/)){     
		ls++;     
	}     
	if (ls > 1){
		ls -= 1;
	}
	console.log(ls);
	return ls
}

function startTiming(w,which, time){
	var timer_num = time;
	if (w==1){
		timeClock=setInterval(function(){
			timer_num--;
			data_btn1.userBtn1 = timer_num + 's';
		   
			if (timer_num == 0) {
				clearInterval(timeClock);
				data_btn1.userBtn1 = '再次发送';
				which.removeAttribute('disabled');
			} 
		},1000)
	}else if(w==2){
		timeClock=setInterval(function(){
			timer_num--;
			data_btn2.userBtn2 = timer_num + 's';
		   
			if (timer_num == 0) {
				clearInterval(timeClock);
				data_btn2.userBtn2 = '再次发送';
				which.removeAttribute('disabled');
			} 
		},1000)
	}
}

function checkAutoLogin(){
	uac = getCookie('uac');
	var input_ac = document.getElementById("UserLogin_form_ac");
	var input_pw = document.getElementById("UserLogin_form_pw");
	var input_cbox = document.getElementById("rememAC");
	if (uac != null && uac != 'null'){
		input_ac.value = getCookie('uac');
		
		str = '';
		for (var i=0;i<parseInt(getCookie('upw_length'));i++){
			str += '1';
		}
		input_pw.value = str;
		input_cbox.checked = true;
	}else{
		input_ac.value = '';
		input_pw.value = '';
		input_cbox.checked = false;
	}
	
}
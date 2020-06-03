function pageInit(){
	document.body.style.backgroundImage = "url(/static/img/BG.png)";
	
	
	// 如果注册成功,利用返回的Token自动登录
	checkRegisterResult();
	
	topNavInit();
}

function checkRegisterResult(){
	if (suc == 'true'){
		// 注册成功
		saveToken(newToken);
		alert('注册成功,您已自动登录');
		showRetPage(1);
	}else if(suc == 'false'){
		alert('注册失败');
		showRetPage(2);
	}
}

function showRetPage(w){
	var p1 = document.getElementById("register_result");
	var p2 = document.getElementById("register_result_fail");
	if (w == 1){
		p1.style.display = 'flex';
		p2.style.display = 'none';
	}else if ( w==2 ){
		p2.style.display = 'flex';
		p1.style.display = 'none';
	}
}

function register_showPW(){
	var input = document.getElementById("register_pw");
	if(input.type === "password"){
		input.type = "text"
	}else{
		input.type = "password"
	}
}
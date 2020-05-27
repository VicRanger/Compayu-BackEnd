function pageInit(){
	document.body.style.backgroundImage = "url(/static/img/BG.png)";
	
	topNavInit();
	
	titleInit();
}

function titleInit(){
	var nickname = getCookie('nickname');
	if (nickname.length>=6){
		nickname = nickname.slice(0,5)+'...';
	}
	document.title = "Compayu | " + nickname + "的个人空间";
}
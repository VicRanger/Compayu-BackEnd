function pageInit() {
	document.body.style.backgroundImage = "url(/static/img/BG.png)";

	userCenter_checkLogin();

	topNavInit();

	titleInit();

	setUserData(1);

	bindKeyPress();

	initSwitchBtn();
}

// 更改网页title
function titleInit() {
	var nickname = '我';
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		async: false, //同步的方式,获取结果在继续下面的步骤
		data: {
			'what': 'nickname',
			'token': getToken(),
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200') {
				nickname = ret.data;
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			//console.log(errorThrown);
		}
	});
	if (nickname.length >= 6) {
		nickname = nickname.slice(0, 5) + '...';
	}
	document.title = "Compayu | " + nickname + "的个人空间";
}


//上传头像
function changeAvatar() {
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
			$('#userCenter_avatar').attr('src', fileReader.result)
		}
	})
}

function uploadAvatar() {
	var formdata = new FormData();
	formdata.append("avatar", $("#avatar_input")[0].files[0]);
	formdata.append('token', getToken());
	$.ajax({
		processData: false,
		contentType: false,
		url: '/api/avatar/',
		type: 'post',
		data: formdata,
		dataType: "json",
		success: function (arg) {
			if (ret.code == '200') {
				userinfo = ret;
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function () {
			//alert("访问繁忙，请重试")
		}
	})
}

//上传新的签名
function changeSignature(sig) {
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
			'what': 'setuser',
			'where': 'signature',
			'data': sig,
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200') {
				alert('修改成功');
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});
}

// 绑定按键输入
function bindKeyPress() {
	$('#userCenter_signature').bind('keydown', function (event) {
		if (event.keyCode == "13") {
			var sig = document.getElementById("userCenter_signature");
			changeSignature(sig.value);
		}
	});
	showMostView(1);

	$('#userCenter_searchThought').bind('keydown', function (event) {
		if (event.keyCode == "13") {
			searchThought();
		}
	});
	document.getElementById("userCenter_searchThought").value = '';
}

function logout() {
	$.ajax({
		url: '/user/logout/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			jumpToIndex();
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});
}

function initSwitchBtn() {
	var btns_p = document.getElementsByClassName("userCenter_btn_p");
	var page = 0;
	page = getPage();

	for (var i = 0; i < btns_p.length; i++) {
		if (i == page) {
			btns_p[i].style.color = '#4169E1';
		} else {
			btns_p[i].style.color = "black";
		}
	}
	// 滑块
	var subline = document.getElementById("userCenter_subline");
	var left = 10 + (10 + 160) * page;
	subline.style.marginLeft = left + 'px';
}

function userCenter_checkLogin() {
	var isLogin = checkLogin();
	if (isLogin == "False") {
		alert("您的账号状态异常,请重新登录");
		jumpToLogin();
	}
}

function switchBtn_hover(w) {
	if (w == 0) {
		//归位
		initSwitchBtn();
	} else {
		var btns_p = document.getElementsByClassName("userCenter_btn_p");
		btns_p[w - 1].style.color = '#4169E1';
		// 滑块
		var subline = document.getElementById("userCenter_subline");
		var left = 10 + (10 + 160) * (w - 1);
		subline.style.marginLeft = left + 'px';
	}
}

function userCenter_changePage(p) {
	if (p == 1) {
		window.location.href = '/user/usercenter/?which=myinfo';
	} else if (p == 2) {
		window.location.href = '/user/usercenter/?which=mymessage';
	} else if (p == 3) {
		window.location.href = '/user/usercenter/?which=mysafety';
	} else if (p == 4) {
		window.location.href = '/user/usercenter/?which=mynews';
	} else if (p == 5) {
		window.location.href = '/user/usercenter/?which=mystar';
	}
}

function getPage() {
	var page = 0;
	if (which == 'myinfo') {
		// 第一页
		page = 0;
	} else if (which == 'mymessage') {
		page = 1;
	} else if (which == 'mysafety') {
		page = 2;
	} else if (which == 'mynews') {
		page = 3;
	} else if (which == 'mystar') {
		page = 4;
	}
	return page;
}

function showSubmitBtn() {
	var btn = document.getElementById("submitBtn_myinfo");
	btn.style.display = 'flex';
	setTimeout(function () {
		btn.style.opacity = '1';
	}, 300);
}

function myinfoSubmit() {
	var gender = 0;
	var boy = document.getElementById("userCenter_boy");
	var girl = document.getElementById("userCenter_girl");
	if (boy.checked) {
		gender = 1;
	} else if (girl.checked) {
		gender = 2;
	}
	var birthday = document.getElementById("userCenter_birthday").value;
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
			'what': 'setuser',
			'where': 'genderAndBirthday',
			'gender': gender,
			'birth': birthday,
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200') {
				alert('修改成功');
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});
}

function showMostView(w) {
	var b1 = document.getElementById("thoughtMostView");
	var b2 = document.getElementById("thoughtNewest");
	var subline = document.getElementById("thoughtSubline");
	var p1 = document.getElementById("userCenter_thought_mostview");
	var p2 = document.getElementById("userCenter_thought_newest");
	if (w == 1) {
		b1.style.color = "#2244CC";
		b2.style.color = "black";
		subline.style.marginLeft = '0%';
		p1.style.display = 'flex';
		p2.style.display = 'none';
	} else if (w == 2) {
		b1.style.color = "black";
		b2.style.color = "#2244CC";
		subline.style.marginLeft = '35%';
		p2.style.display = 'flex';
		p1.style.display = 'none';
	}
}

// 填入用户现在的信息
function setUserData(page) {
	// 头像
	var avatar = document.getElementById("userCenter_avatar");
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		data: {
			'token': getToken(),
			'what': 'avatar',
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200' && ret.data != 'https://cdn.wzz.ink/avatar/defaultAvatar.png') {
				avatar.setAttribute('src', ret.data);
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});
	// user
	var userinfo;
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		async: false,
		data: {
			'token': getToken(),
			'what': 'userinfo',
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200') {
				console.log(ret);
				userinfo = ret;

			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});
	document.getElementById("userType").innerHTML = userinfo.usertype;
	document.getElementById("userLevel").innerHTML = "LV" + parseInt(userinfo.level / 100);
	document.getElementById("userCenter_nickname").innerHTML = userinfo.nickname;
	document.getElementById("userCenter_signature").value = userinfo.signature;
	var gender = userinfo.gender;
	var boxObj = document.getElementById('otherInfo');
	if (gender == 1) {
		var genderImg = document.createElement('img');
		genderImg.setAttribute('src', '/static/img/userCenter_boy.png');
		genderImg.setAttribute('class', 'userCenter_up_icon');
		genderImg.setAttribute("title", '糙汉子')
		boxObj.appendChild(genderImg);
	} else if (gender == 2) {
		var genderImg = document.createElement('img');
		genderImg.setAttribute('src', '/static/img/userCenter_girl.png');
		genderImg.setAttribute('class', 'userCenter_up_icon');
		genderImg.setAttribute("title", '萌妹子')
		boxObj.appendChild(genderImg);
	}
	if (userinfo.email) {
		var email = document.getElementById("userCenter_up_email");
		email.setAttribute('src', "/static/img/email_on.png");
	}
	if (userinfo.phone) {
		var phone = document.getElementById("userCenter_up_phone");
		phone.setAttribute('src', "/static/img/phone_on.png");
	}
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		async: false,
		data: {
			'token': getToken(),
			'what': 'jitang',
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			if (ret.code == '200') {
				if (ret.data) {
					document.getElementById("userCenter_jitang_p").innerHTML = ret.data;
				}
			} else if (ret.code == '403') {
				isLogin = 'False';
				alert("你的登录已过期,请重新登录");
				jumpToLogin();
			}
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	});

	page = getPage();
	// 按页码填充数据
	if (page == 0) {
		// 个人主页
		var thisPage = document.getElementById("userCenter_myinfo");
		thisPage.style.display = 'flex';

		document.getElementById("userCenter_level_p").innerHTML = "LV" + parseInt(userinfo.level / 100);
		var exp = userinfo.level % 100;
		document.getElementById("userCenter_exp").innerHTML = exp + "/100";
		document.getElementById("userCenter_level_line").style.width = exp + "%";
		var boy = document.getElementById("userCenter_boy");
		var girl = document.getElementById("userCenter_girl");
		boy.checked = false;
		girl.checked = false;
		if (gender == 1) {
			boy.checked = true;
		} else if (gender == 2) {
			girl.checked = true;
		}
		$('#userCenter_birthday').val(userinfo.birthday);

		var mythought;
		$.ajax({
			url: '/api/user/',
			type: 'POST', //HTTP请求类型
			timeout: 5000, //超时时间设置为10秒；
			dataType: "json",
			async: false,
			data: {
				'token': getToken(),
				'what': 'thought',
				'where': 'mostView',
			}, // data是必须的,可以空,不能没有
			success: function (ret) {
				if (ret.code == '200') {
					mythought = ret;
				} else if (ret.code == '403') {
					isLogin = 'False';
					alert("你的登录已过期,请重新登录");
					jumpToLogin();
				}
			},
			error: function (xhr, type, errorThrown) {
				console.log(errorThrown);
			}
		});
		var page1 = document.getElementById("userCenter_thought_mostview");
		// 先删除对应个数的元素
		for (var i = 0; i < mythought.num; i++) {
			var rows = page1.children;
			rows[0].parentNode.removeChild(rows[0]);
		}
		// 在添加对应个数的元素
		for (var i = 0; i < mythought.num; i++) {
			var newRow = createThoughtRow(mythought.data[i], i + 1);
			page1.appendChild(newRow);
		}

		$.ajax({
			url: '/api/user/',
			type: 'POST', //HTTP请求类型
			timeout: 5000, //超时时间设置为10秒；
			dataType: "json",
			async: false,
			data: {
				'token': getToken(),
				'what': 'thought',
				'where': 'newest',
			}, // data是必须的,可以空,不能没有
			success: function (ret) {
				if (ret.code == '200') {
					mythought = ret;
				} else if (ret.code == '403') {
					isLogin = 'False';
					alert("你的登录已过期,请重新登录");
					jumpToLogin();
				}
			},
			error: function (xhr, type, errorThrown) {
				console.log(errorThrown);
			}
		});
		var page2 = document.getElementById("userCenter_thought_newest");
		// 先删除对应个数的元素
		for (var i = 0; i < mythought.num; i++) {
			var rows = page2.children;
			rows[0].parentNode.removeChild(rows[0]);
		}
		// 在添加对应个数的元素
		for (var i = 0; i < mythought.num; i++) {
			var newRow = createThoughtRow(mythought.data[i], i + 1);
			page2.appendChild(newRow);
		}
	} else if (page == 1) {
		// 我的想法页面
		var thisPage = document.getElementById("userCenter_mythought");
		thisPage.style.display = 'flex';
		// 初始化第一页
		setCookie('page', 1);
		changeFilter('time');

		count = document.getElementsByClassName('mythought_countp');
		$.ajax({
			url: '/api/user/',
			type: 'POST', //HTTP请求类型
			timeout: 5000, //超时时间设置为10秒；
			dataType: "json",
			async: false,
			data: {
				'token': getToken(),
				'what': 'thoughtcount',
			}, // data是必须的,可以空,不能没有
			success: function (ret) {
				if (ret.code == '200') {
					count[0].innerHTML = "总浏览量:" + ret.vnum;
					count[1].innerHTML = "发送想法数:" + ret.tnum;
				} else if (ret.code == '403') {
					isLogin = 'False';
					alert("你的登录已过期,请重新登录");
					jumpToLogin();
				}
			},
			error: function (xhr, type, errorThrown) {
				console.log(errorThrown);
			}
		});
	} else if (page == 2) {

	}
}


function createThoughtRow(thought, i) {
	// 用js拼接一个预览的小窗口出来,再输出
	//console.log(thought);

	var row = document.createElement('div');
	row.setAttribute('class', 'userCenter_thoughtRow');
	row.setAttribute('onclick', 'changeThought(' + thought.id + ',' + thought.rich_text + ')');
	// 四种心情的颜色 happy #FFA8DF
	var colorWithMood = {
		'happy': '#f88bff',
		'angry': '#ffc28b',
		'disgust': '#a1ff8b',
		'sad': '#7182ff'
	};

	var num = document.createElement('div');
	num.setAttribute('class', 'thoughtRow_num');
	var moodColor = colorWithMood[thought.type_raw];
	num.style.background = moodColor;
	var num_p = document.createElement('p');
	num_p.setAttribute('class', 'thoughtRow_num_p');
	num_p.innerHTML = i;
	num.appendChild(num_p);
	var num_view = document.createElement('div');
	num_view.setAttribute('class', 'thoughtRow_views');
	var num_view_img = document.createElement('img');
	num_view_img.setAttribute('class', 'thoughtRow_viewIcon');
	num_view_img.setAttribute('src', '/static/img/userCenter_viewsIcon.png');
	num_view.appendChild(num_view_img);
	var num_view_p = document.createElement('p');
	num_view_p.setAttribute('class', 'thoughtRow_views_p');
	num_view_p.innerHTML = thought.views;
	num_view.appendChild(num_view_p);
	num.appendChild(num_view);
	row.appendChild(num);

	var title = document.createElement('div');
	title.setAttribute('class', 'thoughtRow_title');
	var title_p1 = document.createElement('p');
	title_p1.setAttribute('class', 'thoughtRow_title_p');
	title_p1.innerHTML = thought.title;
	title.appendChild(title_p1);
	var title_div = document.createElement('div');
	title_div.style.width = '100%';
	title_div.style.background = 'rgba(0,0,0,0.25)';
	title_div.style.height = '2%';
	title.appendChild(title_div);
	var title_date = document.createElement("div");
	title_date.setAttribute('class', 'thoughtRow_time');
	title_date.innerHTML = thought.create_time.split('T')[0];
	title.appendChild(title_date);
	row.appendChild(title);

	var div = document.createElement('div');
	div.style.background = 'rgba(0,0,0,0.25)';
	div.style.height = '70%';
	div.style.width = '1px';
	row.appendChild(div);

	var text = document.createElement('div');
	text.setAttribute('class', 'thoughtRow_text');
	var text_cont = document.createElement('div');
	text_cont.setAttribute('class', 'thoughtRow_text_container');
	text.appendChild(text_cont);
	var text_p = document.createElement('p');
	text_p.setAttribute('class', 'thoughtRow_text_p');
	$.ajax({
		url: '/api/user/',
		type: 'POST', //HTTP请求类型
		timeout: 5000, //超时时间设置为10秒；
		dataType: "json",
		async: false,
		data: {
			'id': thought.rich_text,
			'token': getToken(),
			'what': 'thoughtContent',
		}, // data是必须的,可以空,不能没有
		success: function (ret) {
			text_p.innerHTML = ret.text;
		},
		error: function (xhr, type, errorThrown) {
			console.log(errorThrown);
		}
	})
	text_cont.appendChild(text_p);
	row.appendChild(text);

	row.appendChild(div);

	var control = document.createElement('div');
	control.setAttribute('class', 'thoughtRow_control');
	var changeBtn = document.createElement('input');
	var deleteBtn = document.createElement('input');
	changeBtn.setAttribute('class', 'thoughtRow_btn1');
	changeBtn.setAttribute('type', 'button');
	changeBtn.setAttribute('value', '修改');
	changeBtn.setAttribute('onclick', 'changeThought(' + thought.id + ',' + thought.rich_text + ')');
	deleteBtn.setAttribute('class', 'thoughtRow_btn2');
	deleteBtn.setAttribute('type', 'button');
	deleteBtn.setAttribute('value', '删除');
	deleteBtn.setAttribute('onclick', 'deleteThought(' + thought.id + ',' + thought.rich_text + ')');

	control.appendChild(changeBtn);
	control.appendChild(deleteBtn);
	row.appendChild(control);

	return row;
}

function deleteThought(tid, cid) {
	console.log("删除id" + tid);
}

function changeThought(tid, cid) {
	console.log("修改id" + tid);
}

// 根据过滤条件显示想法
function fiilData_thought(filter) {
	var mythought;
	setCookie('filter', filter);
	page = getCookie('page');
	if (filter != 'search') {
		$.ajax({
			url: '/api/user/',
			type: 'POST', //HTTP请求类型
			timeout: 5000, //超时时间设置为10秒；
			dataType: "json",
			async: false,
			data: {
				'token': getToken(),
				'what': 'thought',
				'where': 'filter',
				'filter': filter,
				'page': page,
			}, // data是必须的,可以空,不能没有
			success: function (ret) {
				if (ret.code == '200') {
					mythought = ret;
				} else if (ret.code == '403') {
					isLogin = 'False';
					alert("你的登录已过期,请重新登录");
					jumpToLogin();
				}
			},
			error: function (xhr, type, errorThrown) {
				console.log(errorThrown);
			}
		});

		var container = document.getElementById("mythoughtList");
		// 总页数
		var pagenum = parseInt(mythought.num / 10) + 1;
		setCookie('pagenum', pagenum);
		setPageBtn(pagenum);
		// 先清空表单
		var childs = container.childNodes;
		for (var i = childs.length - 1; i >= 0; i--) {
			container.removeChild(childs[i]);
		}

		// 在添加对应个数的元素
		for (var i = 0; i < mythought.data.length; i++) {
			var newRow = createThoughtRow(mythought.data[i], i + 1);
			container.appendChild(newRow);
		}
	} else {
		var search = document.getElementById('userCenter_searchThought').value;
		$.ajax({
			url: '/api/user/',
			type: 'POST', //HTTP请求类型
			timeout: 5000, //超时时间设置为10秒；
			dataType: "json",
			async: false,
			data: {
				'token': getToken(),
				'what': 'thought',
				'where': 'filter',
				'filter': filter,
				'page': page,
				'search': search,
			}, // data是必须的,可以空,不能没有
			success: function (ret) {
				if (ret.code == '200') {
					mythought = ret;
				} else if (ret.code == '403') {
					isLogin = 'False';
					alert("你的登录已过期,请重新登录");
					jumpToLogin();
				}
			},
			error: function (xhr, type, errorThrown) {
				console.log(errorThrown);
			}
		});

		var container = document.getElementById("mythought_searchResult");
		// 总页数
		var pagenum = parseInt(mythought.num / 10) + 1;
		setCookie('pagenum', pagenum);
		setPageBtn(pagenum);

		document.getElementById("mythought_searchNum_p").innerHTML = "共搜索到&emsp;" + mythought.num + "&emsp;个结果";

		// 先清空表单
		var childs = container.childNodes;
		for (var i = childs.length - 1; i >= 0; i--) {
			container.removeChild(childs[i]);
		}

		// 在添加对应个数的元素
		for (var i = 0; i < mythought.data.length; i++) {
			var newRow = createThoughtRow(mythought.data[i], i + 1);
			container.appendChild(newRow);
		}
	}
}

function changeFilter(filter) {
	var btnlist = document.getElementsByClassName('mythought_filterBtn');
	var subline = document.getElementById("mythought_chooceFilter_subline");
	var w = 0;
	if (filter == 'time') {
		w = 0;
	} else if (filter == 'view') {
		w = 1;
	} else if (filter == 'search') {
		w = 2;
	}
	for (var i = 0; i < btnlist.length; i++) {
		if (i == w) {
			btnlist[i].style.color = '#4169E1';
		} else {
			btnlist[i].style.color = '#111111';
		}
	}
	subline.style.marginLeft = 130 * w + 'px';
	var p1 = document.getElementById("mythoughtList");
	var p2 = document.getElementById("mythoughtSearchList");
	if (w == 2) {
		p2.style.display = 'flex';
		p1.style.display = 'none';
	} else {
		p1.style.display = 'flex';
		p2.style.display = 'none';
	}
	fiilData_thought(filter);
}

function thoughtChangePage(p) {
	setCookie('page', p);
	fiilData_thought(getCookie('filter'));
}

function leftAndRightPage(w) {
	page = parseInt(getCookie('page'));
	if (w == 1) {
		if (page > 1) {
			page -= 1;
			setCookie('page', page);
			fiilData_thought(getCookie('filter'));
		}
	} else if (w == 2) {
		if (page < getCookie('pagenum')) {
			page += 1;
			setCookie('page', page);
			fiilData_thought(getCookie('filter'));
		}
	}
}

function setPageBtn(pagenum) {
	var cont = document.getElementById("mythought_pageContainer");
	var page = getCookie('page');
	// 先清空再生成
	var childs = cont.childNodes;
	for (var i = childs.length - 1; i >= 0; i--) {
		cont.removeChild(childs[i]);
	}

	var last = document.createElement('img');
	last.setAttribute('class', 'mythought_imgBtn');
	last.setAttribute('src', '/static/img/userCenter_lastpage.png');
	last.setAttribute('onclick', 'leftAndRightPage(1)');
	cont.appendChild(last);

	for (var i = 0; i < pagenum; i++) {
		var child = createPageBtn(i + 1);
		if (i + 1 == page) {
			child.setAttribute('class', 'mythought_page_active');
		}
		cont.appendChild(child);
	}

	var next = document.createElement('img');
	next.setAttribute('class', 'mythought_imgBtn');
	next.setAttribute('src', '/static/img/userCenter_nextpage.png');
	next.setAttribute('onclick', 'leftAndRightPage(2)');
	cont.appendChild(next);
}

function createPageBtn(page) {
	var div = document.createElement('div');
	div.setAttribute('class', 'mythought_page');
	var p = document.createElement('p');
	p.innerHTML = page;
	div.appendChild(p);
	div.setAttribute('onclick', 'thoughtChangePage(' + page + ')');
	return div;
}

function searchThought() {
	var search = document.getElementById('userCenter_searchThought').value;
	var page = getCookie('page');
	if (search != '') {
		setCookie('search', search);
		changeFilter('search');

	} else {
		alert("请输入有效值");
	}
}
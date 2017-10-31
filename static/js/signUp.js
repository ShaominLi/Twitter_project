function register() {
	if(!checkname()){
		return false;	
	}
	if (!checkpass()) {
		return false;
	} 
	if(!checkemail()){
		return false;
	} 
	return true;
}

function checkname()    
{
    var name = $("#uname").val();  
    var ts = document.getElementById("nametext");
    if(name == "")    
    {   
        ts.innerHTML ="input name!";
        ts.style.color="red";
        return false;
    }
    return true;
}

function checkpass(){
	var userPass = $("#upass").val();
	
	var pts = document.getElementById("pswtext");
	/*
	if(userPass == "")
	{
		pts.innerHTML ="input password!";
		pts.style.color="red";
	    return false;
	}else */
	if(userPass.length<6)	
	{	
		pts.innerHTML ="password short!";
		pts.style.color="red";
	    return false;
	}else
		return checkrpass();
}
function checkrpass(){
	var userPass = $("#upass").val();
	var userRPass = $("#urpass").val();
	var prts =  document.getElementById("rpswtext");
	if (userPass != userRPass) {
		prts.innerHTML="different inputs!";
		prts.style.color="red";
		return false;
	}
	return true;
}
function checkemail(){
	var userEmail = $("#uemail").val();
	var ets = document.getElementById("emailtext");
	if(!isEmail(userEmail)){
		ets.innerHTML ="format incorrect!";
		ets.style.color="red";
		return false;
	} 
	return true;
}
function isEmail(str){
    var reg = /[a-z0-9-]{1,30}@[a-z0-9-]{1,65}.[a-z]{3}/;
    return reg.test(str);
}


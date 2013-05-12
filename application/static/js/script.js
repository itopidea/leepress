function dateToString(date,format){
	/**
	:param data:seconds from 1970/1/1
	:param format:date format like "yyyy-MM-dd hh:mm:ss" or "yyyy-M-d h:m:s" 
	**/
	date=date*1000;
	date=new Date(date);
	// date.setTime(date);
	var z = {

		M:date.getMonth()+1,
		d:date.getDate(),
		h:date.getHours(),
		m:date.getMinutes(),
		s:date.getSeconds()};
	format = format.replace(
		/(M+|d+|h+|m+|s+)/g,
		function(v) {
			return ((v.length>1?"0":"")+eval('z.'+v.slice(-1))).slice(-2)});
	return format.replace(
		/(y+)/g,function(v) {return date.getFullYear().toString().slice(-v.length)});
}

//change filesize(int) to String.
function intSizeToString(size){
	if (size==-1){
		return "文件夹";
	}
	else if(size/1024<1)
		return(String(size)+"B");
	else if(size/1024/1024<1){
		size=String(size/1024);
		size=size.substring(0,size.indexOf('.')+2);
		size=size+"KB";
	}
	else if(size/1024/1024/1024<1){
		size=String(size/1024/1024);
		size=size.substring(0,size.indexOf('.')+2);
		size=size+"MB";
	}
	else {
		size=String(size/1024/1024/1024);
		size=size.substring(0,size.indexOf('.')+2);
		size=size+"GB";
	}
	return size;
}

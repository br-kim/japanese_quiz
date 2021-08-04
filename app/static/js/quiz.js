function urlToFileName(url){
    let splited_url = url.split("/");
    return splited_url[splited_url.length - 1].split(".")[0];
}
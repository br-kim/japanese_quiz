
function urlToFileName(url){
    splited_url = url.split("/");
    result = splited_url[splited_url.length - 1].split(".")[0];
    return result;
}



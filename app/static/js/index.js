async function RequestToServer(url, method){
        if (!btnFunction.tokenHeader) {
            alert("토큰 없음");
            return;
        }
        res = await fetch(url,{
            headers: btnFunction.tokenHeader,
            method: method
        });

        return await res;
        // document.body.innerHTML = await res.text();
        // location.reload();
        // domParser = new DOMParser();
        // domParser.parseFromString(await res.text(), "text/html");
    };

let indexScope = {
    loginFunction : async function (){

    }
}
let tokenHeader = {'Content-Type': 'application/json',
        'Authorization' : localStorage.getItem("jpn_quiz_access_token")};
export let serverBaseUrl = window.location.origin;

export async function requestToServer(url, method, is_auth=true){
        if ((is_auth) && (!tokenHeader)) {
            alert("토큰 없음");
            return;
        }
        let header = is_auth ? tokenHeader : {};
        let res = await fetch(url,{
            headers: header,
            method: method
        });
        return res;
       }

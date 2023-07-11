import {requestToServer, serverBaseUrl} from "./index.js";


export async function loginFunction(){
    let login_url = await requestToServer(serverBaseUrl+"/login", "GET", false);
    console.log();
    let url = await login_url.json();
    window.location.href = url;
}

export async function usingCode(){
    // 현재 페이지의 URL
    console.log("usingCode");
    const url = new URL(window.location.href);

    // URLSearchParams 객체 생성
    const searchParams = new URLSearchParams(url.search);

    // code 쿼리 파라미터 값 가져오기
    const code = searchParams.get('code');
    if (!code) {
        return;
    }

    const apiUrl = `${serverBaseUrl}/oauth?code=${code}`;

    let res = await requestToServer(apiUrl, "GET", false);
    let token = await res.json();
    localStorage.setItem("jpn_quiz_access_token",token);
    window.location.href = serverBaseUrl;
}
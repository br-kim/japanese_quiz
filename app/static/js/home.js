import {requestToServer, serverBaseUrl} from "./index.js";


export async function loginFunction(){
    let login_url = await requestToServer(serverBaseUrl+"/login", "GET", false);
    let url = await login_url.json();
    window.location.href = url;
}

export async function usingCode(){
    // 현재 페이지의 URL
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

export async function generateNav() {
    function createAElement(className, href, text, id=null){
        let element = document.createElement("a");
        if (className){
            element.classList.add(className);
        }
        if (href){
            element.href = href;
        }
        if (text){
            element.textContent = text;
        }
        if (id){
            element.id = id;
        }

        return element;
    }
    let navMenuRight = "nav-menu-right";
    let navMenu = "nav-menu";

    let navDiv = document.getElementById("nav-content");

    let mainNav = createAElement(navMenu, "/", "메인");
    let infNav = createAElement(navMenu, "/quiz", "무한모드");
    let testNav = createAElement(navMenu, "/newquiz", "테스트");
    let freeboardNav = createAElement(navMenu, "/fb", "자유게시판");
    let chattingNav = createAElement(navMenu, "/ws", "채팅");
    let loginNav = createAElement(navMenuRight, null, "로그인", "nav-login");
    let logoutNav = createAElement(navMenuRight, "/logout", "로그아웃");
    logoutNav.addEventListener("click", () => {
        localStorage.removeItem("jpn_quiz_access_token");
    });

    navDiv.appendChild(mainNav);
    navDiv.appendChild(infNav);
    navDiv.appendChild(testNav);
    navDiv.appendChild(freeboardNav);
    navDiv.appendChild(chattingNav);

    if (localStorage.getItem("jpn_quiz_access_token")) {
        let res = await requestToServer(serverBaseUrl+"/user-info", "GET");
        if (res.status === 403){
            let errorMsg = await res.json();
            if (errorMsg.detail === "Token Expire"){
                alert("로그인이 만료되었습니다.");
                localStorage.removeItem("jpn_quiz_access_token");
                loginNav.addEventListener("click", loginFunction);
                navDiv.append(loginNav);
                return;
            }
            else{
                alert("처리되지 않은 에러입니다.");
            }
            // localStorage.removeItem("jpn_quiz_access_token");
        }
        let user_email = await res.json();
        localStorage.setItem("user_email", user_email);
        let scoreBoardNav = createAElement(navMenuRight, "/scoreboard", `${user_email}님, 환영합니다!`);
        navDiv.appendChild(scoreBoardNav);
        navDiv.appendChild(logoutNav);
    }
    else{
        loginNav.addEventListener("click", loginFunction);
        navDiv.append(loginNav);
    }
}

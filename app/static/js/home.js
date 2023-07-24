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
            // element.classList.add(className);
            element.classList.add("nav-link");
            element.classList.add("active");
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
        // create li element class nav-item
        let liElement = document.createElement("li");
        liElement.classList.add("nav-item");
        liElement.appendChild(element);
        return liElement;
    }
    let navMenuRight = "nav-menu-right";
    let navMenu = "nav-menu";

    let navDiv = document.getElementById("nav-div");

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
    // create ul element class navbar-nav me-auto mb-2 mb-lg-0
    let ulElement = document.createElement("ul");
    navDiv.appendChild(ulElement);

    ulElement.classList.add("navbar-nav", "me-auto", "mb-2", "mb-lg-0");
    ulElement.appendChild(mainNav);
    ulElement.appendChild(infNav);
    ulElement.appendChild(testNav);
    ulElement.appendChild(freeboardNav);
    ulElement.appendChild(chattingNav);

    // navDiv.appendChild(mainNav);
    // navDiv.appendChild(infNav);
    // navDiv.appendChild(testNav);
    // navDiv.appendChild(freeboardNav);
    // navDiv.appendChild(chattingNav);

    if (localStorage.getItem("jpn_quiz_access_token")) {
        let res = await requestToServer(serverBaseUrl+"/user-info", "GET");
        if (res.status === 403){
            let errorMsg = await res.json();
            if (errorMsg.detail === "Token Expire"){
                alert("로그인이 만료되었습니다.");
                localStorage.removeItem("jpn_quiz_access_token");
                loginNav.addEventListener("click", loginFunction);
                ulElement.appendChild(loginNav);
                // navDiv.append(loginNav);
                return;
            }
            else{
                alert("처리되지 않은 에러입니다.");
            }
            // localStorage.removeItem("jpn_quiz_access_token");
        }
        let userInfoRes = await res.json();
        localStorage.setItem("user_email", userInfoRes.email);
        let scoreBoardNav = createAElement(navMenuRight, "/scoreboard", `${userInfoRes.email}님, 환영합니다!`);
        ulElement.appendChild(scoreBoardNav);
        ulElement.appendChild(logoutNav);

        // navDiv.appendChild(scoreBoardNav);
        // navDiv.appendChild(logoutNav);
    }
    else{
        loginNav.addEventListener("click", loginFunction);
        ulElement.appendChild(loginNav);
        // navDiv.append(loginNav);
    }
}

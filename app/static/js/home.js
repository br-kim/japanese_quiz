import {requestToServer, serverBaseUrl} from "./index.js";


export async function loginFunction() {
    let login_url = await requestToServer(serverBaseUrl + "/login", "GET", false);
    let url = await login_url.json();
    window.location.href = url;
}

export async function usingCode() {
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
    localStorage.setItem("jpn_quiz_access_token", token);
    window.location.href = serverBaseUrl;
}

export async function generateNav() {
    function createAElement(href, text, id = null) {
        let element = document.createElement("a");
        element.classList.add("nav-link");
        element.classList.add("active");
        if (href) {
            element.href = href;
        }
        if (text) {
            element.textContent = text;
        }
        if (id) {
            element.id = id;
        }
        let divElement = document.createElement("div");
        divElement.classList.add("nav-item");
        divElement.appendChild(element);
        return divElement;
    }

    let navDiv = document.getElementById("nav-div");

    let navLeftDiv = document.createElement("div");
    let navRightDiv = document.createElement("div");

    navLeftDiv.classList.add("d-flex", "justify-content-start");
    navRightDiv.classList.add("d-flex", "justify-content-end");

    let mainNav = createAElement("/", "메인");
    let infNav = createAElement("/quiz", "무한모드");
    let testNav = createAElement("/newquiz", "테스트");
    let freeboardNav = createAElement("/fb", "자유게시판");
    let chattingNav = createAElement("/ws", "채팅");
    let loginNav = createAElement(null, "로그인", "nav-login");
    let logoutNav = createAElement("/logout", "로그아웃");
    logoutNav.addEventListener("click", () => {
        localStorage.removeItem("jpn_quiz_access_token");
    });
    let divContainer = document.createElement("div");

    navDiv.appendChild(divContainer);

    divContainer.classList.add("navbar-nav", "mb-2", "mb-lg-0", "w-100", "justify-content-between");
    divContainer.append(navLeftDiv, navRightDiv);

    navLeftDiv.append(mainNav, infNav, testNav, freeboardNav, chattingNav);

    if (localStorage.getItem("jpn_quiz_access_token")) {
        let res = await requestToServer(serverBaseUrl + "/user-info", "GET");
        if (res.status === 403) {
            let errorMsg = await res.json();
            if (errorMsg.detail === "Token Expire") {
                alert("로그인이 만료되었습니다.");
                localStorage.removeItem("jpn_quiz_access_token");
                loginNav.addEventListener("click", loginFunction);
                navRightDiv.appendChild(loginNav);
                return;
            } else {
                alert("처리되지 않은 에러입니다.");
            }
            // localStorage.removeItem("jpn_quiz_access_token");
        }
        let userInfoRes = await res.json();
        localStorage.setItem("user_email", userInfoRes.email);
        let scoreBoardNav = createAElement("/scoreboard", `${userInfoRes.email}님, 환영합니다!`);
        navRightDiv.appendChild(scoreBoardNav);
        navRightDiv.appendChild(logoutNav);
    } else {
        loginNav.addEventListener("click", loginFunction);
        navRightDiv.appendChild(loginNav);
    }
}

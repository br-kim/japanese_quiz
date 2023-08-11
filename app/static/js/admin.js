import {requestToServer, serverBaseUrl} from "./index.js";

async function generateAdminPage() {
    let res = await requestToServer(serverBaseUrl + "/user-info", "GET");
}
async function getUserList() {
    let res = await requestToServer(serverBaseUrl + "/admin/users", "GET", true);
    let userList = await res.json();
    if (res.status !== 200) {
        return;
    }
    let userListIdDiv = document.getElementById("user-list-id-div");
    let userListEmailDiv = document.getElementById("user-list-email-div");

    userListIdDiv.innerHTML = "";
    userListEmailDiv.innerHTML = "";

    for (let user of userList) {
        let userDiv = document.createElement("div");
        userDiv.classList.add("col");
        let userEmailDiv = document.createElement("div");
        userEmailDiv.classList.add("row");
        userEmailDiv.textContent = user.email;
        let userIdDiv = document.createElement("div");
        userIdDiv.classList.add("row");
        userIdDiv.textContent = user.id;
        userListEmailDiv.appendChild(userEmailDiv);
        userListIdDiv.appendChild(userIdDiv);
    }
}

let userListBtn = document.getElementById("user-list-btn");
userListBtn.addEventListener("click", getUserList);
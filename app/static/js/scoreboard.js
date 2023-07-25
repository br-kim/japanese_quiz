import {requestToServer, serverBaseUrl} from "./index.js";

export async function requestScoreBoard(){
    let res = await requestToServer(serverBaseUrl+"/scoreboard/data","GET", true);
    let score_data = await res.json();
    let hiraganaData = score_data.hiragana;
    let katakanaData = score_data.katakana;
    let hiraScoreDiv = document.getElementById("score-board-hiragana");
    let kataScoreDiv = document.getElementById("score-board-katakana");
    let hira = generateScore(hiraganaData);
    let kata = generateScore(katakanaData);
    hiraScoreDiv.appendChild(hira);
    kataScoreDiv.appendChild(kata);
}

function generateScore(data){
    let scoreContainer = document.createElement("div");
    scoreContainer.classList.add("row", "row-cols-2");
    for (let key in data){
        const value = data[key];
        let scoreSetDiv = document.createElement("div");
        scoreSetDiv.classList.add("d-flex", "justify-content-between", "row");
        let scoreDiv = document.createElement("div");
        scoreDiv.classList.add("col");
        let characterDiv = document.createElement("div");
        characterDiv.classList.add("col");
        characterDiv.innerHTML = key;
        scoreDiv.innerHTML = value;
        scoreSetDiv.append(characterDiv, scoreDiv);
        scoreSetDiv.append(document.createElement("hr"));
        scoreContainer.append(scoreSetDiv);
    }
    return scoreContainer;
}
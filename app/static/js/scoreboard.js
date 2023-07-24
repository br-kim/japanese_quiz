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
    for (let key in data){
        const value = data[key];
        let scoreDiv = document.createElement("div");
        scoreDiv.innerHTML = `${key} : ${value}`;
        scoreContainer.appendChild(scoreDiv);
    }
    return scoreContainer;
}
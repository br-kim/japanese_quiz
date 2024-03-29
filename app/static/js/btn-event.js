import {requestToServer, token} from "./index.js";

export let btnFunction = {
    quizPathUrl: '/quiz-data',
    infQuiz: '/random',
    functionContain: null,
    scoreAdd: function (elemId) {
        let score = document.getElementById(elemId).innerText;
        score = Number(score) + 1;
        document.getElementById(elemId).innerText = score;
    },

    buildIncorrectSheetTable: function () {
        let grid = document.getElementById('incorrect-sheet-grid');
        let japaneseCharacterDiv = document.createElement('div');
        let pronDiv = document.createElement('div');
        let incorrectSetDiv = document.createElement('div');
        incorrectSetDiv.classList.add('col');
        incorrectSetDiv.append(japaneseCharacterDiv, pronDiv);
        let characterImg = document.createElement('img');
        characterImg.alt = "image";
        characterImg.src = document.getElementById('quiz').src;
        japaneseCharacterDiv.append(characterImg);
        pronDiv.innerText = document.getElementById('contain-answer').title;
        grid.append(incorrectSetDiv);
    },

    isCorrectInfMode: async function () {
        // 무한 모드에서 정답을 확인하는 함수
        let answer = document.getElementById('answer').value;
        let quiz = document.getElementById('contain-answer').title;
        if (answer === quiz) {
            alert("정답입니다!");
            btnFunction.scoreAdd("correct");

            let req_data = {
                character: document.getElementById('quiz').src,
                quiz_type: location.pathname
            };
            if (token) {
                let res = await requestToServer("/scoreboard/data", "PATCH", true, JSON.stringify(req_data));
            }
            await btnFunction.getRandomImageUrl();
        } else {
            alert("오답입니다! 정답은 " + quiz + "입니다.");
            btnFunction.scoreAdd('incorrect');
            await btnFunction.getRandomImageUrl();
        }
    },

    isCorrectTestMode: async function () {
        // 테스트 모드에서 정답을 확인하는 함수
        let answer = document.getElementById('answer').value;
        let quiz = document.getElementById('contain-answer').title;
        if (answer === quiz) {
            alert("정답입니다!");
            let req_data = {
                character: document.getElementById('quiz').src,
                quiz_type: location.pathname
            };
            let res = await requestToServer(
                "/scoreboard/data", "PATCH", true, JSON.stringify(req_data));
            btnFunction.scoreAdd("correct");
            if (!btnFunction.functionContain) {
                btnFunction.functionContain = await btnFunction.getNextImage();
            } else {
                btnFunction.functionContain();
            }
        } else {
            alert("오답입니다! 정답은 " + quiz + "입니다.");
            btnFunction.scoreAdd('incorrect');
            btnFunction.buildIncorrectSheetTable();
            if (!btnFunction.functionContain) {
                btnFunction.functionContain = await btnFunction.getNextImage();
            } else {
                btnFunction.functionContain();
            }
        }
    },

    showAnswer: function () {
        document.getElementById('show-answer').innerText = "정답은 " +
            document.getElementById('contain-answer').title + "입니다.";
    },

    answerClear: function () {
        document.getElementById('answer').value = "";
        document.getElementById('show-answer').innerText = "";
    },

    getRandomImageUrl: async function () {
        let hira = document.getElementById('inf-hiragana');
        let kata = document.getElementById('inf-katakana');
        let weighted = document.getElementById('is-weighted');
        let url = new URL(btnFunction.quizPathUrl + btnFunction.infQuiz, window.location.origin);
        if (hira.checked && kata.checked) {
            url.searchParams.append('kind', 'all');
        } else if (hira.checked) {
            url.searchParams.append('kind', 'hiragana');
        } else if (kata.checked) {
            url.searchParams.append('kind', 'katakana');
        }
        if (weighted.checked) {
            url.searchParams.append('is_weighted', 'true');
        }
        let req_res = await requestToServer(url.toString(), "GET", false);
        let res_json = await req_res.json();
        let file_url = res_json.path;
        document.getElementById('quiz').src = file_url;
        document.getElementById('contain-answer').title = urlToFileName(file_url);
        btnFunction.answerClear();
    },

    toggleFunc: function () {
        let target = document.getElementById('incorrect-sheet-table');
        if (target.style.visibility === "hidden") {
            target.style.visibility = "visible";
            document.getElementById('toggleBtn').innerText = "접기";
        } else {
            target.style.visibility = "hidden";
            document.getElementById('toggleBtn').innerText = "펼치기";
        }
    },

    getTableData: function () {
        let grid = document.getElementById('incorrect-sheet-grid');
        let arr = [];
        for (let i = 0; i < grid.children.length; i++) {
            let child = grid.children[i];
            if (child.children.length > 0 && child.children[0].children[0].tagName === 'IMG') {
                arr.push(child.children[0].children[0].src);
            }
        }
        return arr;
    },

    requestQuizData: async function () {
        let url = new URL("/quiz-data/test-mode", window.location.origin);
        let params = new URLSearchParams(location.search);
        let ganaType = params.get('kind');
        if (ganaType === null) {
            ganaType = 'all';
        }
        url.searchParams.append('kind', ganaType);
        let r = await requestToServer(url.toString(), "GET", true);
        return await r.json();
    },

    initRefreshBtn: function () {
        if (document.getElementById('refresherBtn') === null) {
            alert("퀴즈가 종료되었습니다.");
            let refreshBtn = document.createElement('button');
            refreshBtn.innerText = "새로 고침";
            refreshBtn.id = "refresherBtn";
            refreshBtn.classList.add("btn", "btn-primary");
            document.getElementById('refresher-container').appendChild(refreshBtn);
            document.getElementById("refresherBtn").addEventListener('click', function () {
                location.reload();
            }, false);
        }
    },

    changeTitleSrc: function (arr, arrNum) {
        document.getElementById("quiz").src = arr[arrNum];
        document.getElementById('contain-answer').title = urlToFileName(arr[arrNum]);
    },

    getNextImage: async function () {
        // 문자 목록 데이터를 가져온 후 순서대로 보여주는 함수
        let arrayNum = 0;
        let res = await this.requestQuizData();
        let chars = res.order;
        btnFunction.changeTitleSrc(chars, arrayNum);
        btnFunction.answerClear();
        return function () {
            arrayNum += 1;
            if (arrayNum < chars.length) {
                btnFunction.changeTitleSrc(chars, arrayNum);
            } else {
                btnFunction.initRefreshBtn();
            }
            btnFunction.answerClear();
        };
    },

    getNextImageIncorrect: function () {
        // 오답 퀴즈 데이터 갖고 온 후 순서대로 보여주는 함수
        let arrayNum = 0;
        let chars = btnFunction.getTableData();
        btnFunction.changeTitleSrc(chars, arrayNum);
        return function () {
            arrayNum += 1;
            if (arrayNum < chars.length) {
                btnFunction.changeTitleSrc(chars, arrayNum);
            } else {
                btnFunction.initRefreshBtn();
            }
            btnFunction.answerClear();
        };
    }
};

const submitBtn = document.getElementById('submitBtn');
if (submitBtn !== null) {
    let url = window.location.pathname;
    let eventListener = null;
    if (url === "/quiz") {
        eventListener = btnFunction.isCorrectInfMode;
    } else {
        eventListener = btnFunction.isCorrectTestMode;
    }
    submitBtn.addEventListener('click', eventListener);
}

const showAnswerBtn = document.getElementById('showAnswerBtn');
if (showAnswerBtn !== null) {
    showAnswerBtn.addEventListener('click', btnFunction.showAnswer);
}

const getRandomImageBtn = document.getElementById('getRandomImageBtn');
if (getRandomImageBtn !== null) {
    getRandomImageBtn.addEventListener('click', btnFunction.getRandomImageUrl);
}

const toggleBtn = document.getElementById('toggleBtn');
if (toggleBtn !== null) {
    toggleBtn.addEventListener('click', btnFunction.toggleFunc);
}

let getNextImageBtn = document.getElementById('getNextImageBtn');
if (getNextImageBtn !== null) {
    (async () => {
        await btnFunction.getNextImage().then(async func => {
            btnFunction.functionContain = await btnFunction.getNextImage();
            getNextImageBtn.addEventListener('click', async () => {
                func();
            });
        });
    })();
}

const incorrectQuizBtn = document.getElementById('incorrectQuizBtn');
if (incorrectQuizBtn !== null) {
    incorrectQuizBtn.addEventListener('click', async () => {
        let func = btnFunction.getNextImageIncorrect();
        let newNextImageBtn = getNextImageBtn.cloneNode(true);
        getNextImageBtn.parentNode.replaceChild(newNextImageBtn, getNextImageBtn);
        getNextImageBtn = document.getElementById('getNextImageBtn');
        btnFunction.functionContain = await btnFunction.getNextImageIncorrect();
        let incorrectSheetTable = document.getElementById('incorrect-sheet-table');
        incorrectSheetTable.innerHTML = "";
        getNextImageBtn.addEventListener('click', () => {
            func();
        }, false);
    }, {once: true});
}

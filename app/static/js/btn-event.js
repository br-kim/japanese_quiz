import {requestToServer} from "./index.js";

export let btnFunction = {
    randomImageUrl : '/quiz/path',
    limitQuizImagesUrl : '/newquiz/path-list',
    quizPathUrl : '/quiz-data',
    limQuiz: '/path-list',
    infQuiz: '/random',
    functionContain : null,
    scoreAdd : function(elemId){
        let score = document.getElementById(elemId).innerText;
        score = Number(score) + 1;
        document.getElementById(elemId).innerText = score;
    },

    buildIncorrectSheetTable : function () {
        let table = document.getElementById('incorrect-sheet-table');
        if (table !== null) {
            let cellList = [];
            let begin = table.rows.length - 2;
            let cellsLength = table.rows[begin].cells.length;
            if (cellsLength > 4) {
                let f = Math.floor(cellsLength / 4);
                begin += 2 * f;
                table.insertRow();
                table.insertRow();
            }

            for (let i = begin; i < begin + 2; i++) {
                cellList.push(table.rows[i].insertCell(-1));
            }
            cellList[0].innerHTML =
                "<img alt='image' src=" + document.getElementById('quiz').src + ">";

            cellList[1].innerText =
                document.getElementById('contain-answer').title;
        }
    },

    isCorrect : async function () {
        let answer = document.getElementById('answer').value;
        let quiz = document.getElementById('contain-answer').title;
        if (answer === quiz) {
            alert("정답입니다!");
            btnFunction.scoreAdd('correct');
            let req_data = {
                csrf_token: csrf_token,
                character: document.getElementById('quiz').src,
                quiz_type: location.pathname
            };
            await fetch('/scoreupdate',{
                method: "PATCH",
                headers: btnFunction.tokenHeader,
                body: JSON.stringify(req_data)}).then(async function(response){
                    if(response.status === 403){
                        alert('csrf 오류입니다.');
                    }else{
                        if(location.pathname === '/quiz') {
                            await btnFunction.getRandomImageUrl();
                        }else{
                            if(!btnFunction.functionContain) {
                                btnFunction.functionContain = await btnFunction.getNextImage();
                            }else{
                                btnFunction.functionContain();
                            }}}});
        }else{
            alert("오답입니다!");
            btnFunction.scoreAdd('incorrect');
             if(location.pathname === '/quiz') {
                 await btnFunction.getRandomImageUrl();
             }else{
                 btnFunction.buildIncorrectSheetTable();
                 if(!btnFunction.functionContain){
                     btnFunction.functionContain = await btnFunction.getNextImage();
                 }else{
                     btnFunction.functionContain();
                 }
             }
        }
        },

    showAnswer : function () {
        document.getElementById('show-answer').innerText = "정답은 " +
            document.getElementById('contain-answer').title + "입니다.";
        },

    answerClear : function () {
        document.getElementById('answer').value = "";
        document.getElementById('show-answer').innerText = "";
        },

    getRandomImageUrl : async function () {
        let hira = document.getElementById('inf-hiragana');
        let kata = document.getElementById('inf-katakana');
        let weighted = document.getElementById('is-weighted');
        let url = new URL(btnFunction.quizPathUrl + btnFunction.infQuiz, window.location.origin);
        if (hira.checked && kata.checked){
            url.searchParams.append('kind','all');
        }else if(hira.checked){
            url.searchParams.append('kind','hiragana');
        }else if(kata.checked){
            url.searchParams.append('kind','katakana');
        }
        if (weighted.checked){
            url.searchParams.append('is_weighted', 'true');
        }
        let req_res = await requestToServer(url.toString(), "GET");
        let res_json = await req_res.json();
        let file_url = res_json.path;
        let csrf_token = res_json.csrf_token;
        document.getElementById('quiz').src = file_url;
        document.getElementById('contain-answer').title = urlToFileName(file_url);
        btnFunction.answerClear();
    },

    toggleFunc : function () {
        let target = document.getElementById('incorrect-sheet-table');
        if (target.style.visibility === "hidden") {
            target.style.visibility = "visible";
            document.getElementById('toggleBtn').innerText = "접기";
        } else {
            target.style.visibility = "hidden";
            document.getElementById('toggleBtn').innerText = "펼치기";
        }
    },

    getTableData : function () {
        let table = document.getElementById('incorrect-sheet-table');
        let arr = [];
        let get_url = (elem) => {
            let url = elem.firstChild.src;
            arr.push(url);
        };
        for (let i = 0; i < table.rows.length; i += 2) {
            let buffer = Array.from(table.rows[i].cells);
            buffer.forEach(get_url);
        }
        return arr;
    },

    requestQuizData : async function () {
        let url = new URL(btnFunction.quizPathUrl + btnFunction.limQuiz,window.location.origin);
        let params = new URLSearchParams(location.search);
        let ganaType = params.get('kind');
        if (ganaType === null){
            ganaType = 'all';
        }
        url.searchParams.append('kind',ganaType);
        let r = await requestToServer(url.toString(), "GET", true);
        return await r.json();
    },

    initRefreshBtn : function (){
        if (document.getElementById('refresherBtn') === null){
            let refreshBtn = document.createElement('button');
            refreshBtn.innerText = "새로 고침";
            refreshBtn.id = "refresherBtn";
            document.getElementById('refresher-container').appendChild(refreshBtn);
            document.getElementById("refresherBtn").addEventListener('click',function (){
                location.reload();
            },false);
        }
    },

    changeTitleSrc : function (arr, arrNum){
        document.getElementById("quiz").src = arr[arrNum];
        document.getElementById('contain-answer').title = urlToFileName(arr[arrNum]);
    },

    getNextImage : async function () {
        let arrayNum = 0;
        let res = await this.requestQuizData();
        let chars = res.order;
        let csrf_token = res.csrf_token;
        btnFunction.changeTitleSrc(chars,arrayNum);
        btnFunction.answerClear();
        return function () {
            arrayNum += 1;
            if (arrayNum < chars.length) {
                btnFunction.changeTitleSrc(chars,arrayNum);
            } else {
                btnFunction.initRefreshBtn();
            }
            btnFunction.answerClear();
        };
    },

    getNextImageIncorrect : function () {
        let arrayNum = 0;
        let chars = btnFunction.getTableData();
        btnFunction.changeTitleSrc(chars,arrayNum);
        return function () {
            arrayNum += 1;
            if (arrayNum < chars.length) {
                btnFunction.changeTitleSrc(chars,arrayNum);
            } else {
                btnFunction.initRefreshBtn();
            }
            btnFunction.answerClear();
        };
    },
};

const submitBtn = document.getElementById('submitBtn');
if (submitBtn !== null){
    submitBtn.addEventListener('click',btnFunction.isCorrect,false);
}

const showAnswerBtn = document.getElementById('showAnswerBtn');
if (showAnswerBtn !== null){
    showAnswerBtn.addEventListener('click',btnFunction.showAnswer,false);
}

const getRandomImageBtn = document.getElementById('getRandomImageBtn');
if (getRandomImageBtn !== null) {
    getRandomImageBtn.addEventListener('click', btnFunction.getRandomImageUrl,false);
}

const toggleBtn = document.getElementById('toggleBtn');
if (toggleBtn !== null){
    toggleBtn.addEventListener('click',btnFunction.toggleFunc,false);
}

const getNextImageBtn = document.getElementById('getNextImageBtn');
if (getNextImageBtn !== null) {
    (async() => {
        await btnFunction.getNextImage().then(func =>{
            getNextImageBtn.addEventListener('click', async () => {func();}, false);
        });
    })();
}

const incorrectQuizBtn = document.getElementById('incorrectQuizBtn');
if (incorrectQuizBtn !== null){
    incorrectQuizBtn.addEventListener('click', function () {
        let func = btnFunction.getNextImageIncorrect();
        const incorrectQuizNextBtn = document.getElementById('incorrectQuizNextBtn');
        if (incorrectQuizNextBtn !== null){
            incorrectQuizNextBtn.addEventListener('click', function () {
                func();},false);}
        },{once:true});
}

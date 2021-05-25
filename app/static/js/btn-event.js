let btnFunction = {

    randomImageUrl : '/quiz/path',
    limitQuizImagesUrl : '/newquiz/path-list',
    quizPathUrl : '/quizdata',
    limQuiz: '/path-list',
    infQuiz: '/path',

    scoreAdd : function(elemId){
        let score = document.getElementById(elemId).innerText;
        score = Number(score) + 1;
        document.getElementById(elemId).innerText = score;
    },

    isCorrect : function () {
        answer = document.getElementById('answer').value;
        quiz = document.getElementById('contain-answer').title;
        if (answer === quiz) {
            alert("정답입니다!");
            btnFunction.scoreAdd('correct');
            document.getElementsByClassName('getNextBtn')[0].click();
        } else {
            alert("오답입니다!");
            btnFunction.scoreAdd('incorrect');
            table = document.getElementById('incorrect-sheet-table');
            if (table !== null){
                CellList = [];
                begin = table.rows.length - 2;
                cellsLength = table.rows[begin].cells.length;
                if (cellsLength > 4) {
                    f = Math.floor(cellsLength / 4);
                    begin += 2 * f;
                    table.insertRow();
                    table.insertRow();
                }

                for (let i = begin; i < begin + 2; i++) {
                    CellList.push(table.rows[i].insertCell(-1));
                }
                CellList[0].innerHTML =
                    "<img alt='image' src=" + document.getElementById('quiz').src + ">";

                CellList[1].innerText =
                    document.getElementById('contain-answer').title;
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
        let url = new URL(btnFunction.quizPathUrl + btnFunction.infQuiz,'http://'+window.location.host);
        if (hira.checked && kata.checked){
            url.searchParams.append('kind','all');
        }
        else if(hira.checked){
            url.searchParams.append('kind','hiragana');
        }
        else if(kata.checked){
            url.searchParams.append('kind','katakana');
        }
        new_url = await fetch(url);
        data = new_url.text();
        json = JSON.parse(await data);
        file_url = json["path"];
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
        for (let i = 0; i < table.rows.length; i += 2) {
            buffer = Array.from(table.rows[i].cells);
            buffer.forEach(function (elem) {
                let url = elem.firstChild.src;
                arr.push(url);
            });
        }
        return arr;
    },

    requestQuizData : async function () {
        let url = new URL(btnFunction.quizPathUrl + btnFunction.limQuiz,'http://'+window.location.host);
        let params = new URLSearchParams(location.search);
        let ganaType = params.get('kind');
        if (ganaType === 'all'){
            url.searchParams.append('kind',ganaType);
        }
        else if (ganaType === 'hiragana'){
            url.searchParams.append('kind',ganaType);
        }
        else if (ganaType === 'katakana'){
            url.searchParams.append('kind',ganaType);
        }

        let r = await fetch(url);
        let j = await r.json();
        return j['order'];
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
        let chars = await this.requestQuizData();
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
        func1 = await btnFunction.getNextImage();
    })();
    getNextImageBtn.addEventListener('click', async () => {
        func1();
    }, false);
}

const incorrectQuizBtn = document.getElementById('incorrectQuizBtn');
if (incorrectQuizBtn !== null){
    incorrectQuizBtn.addEventListener('click', function () {
        func2 = btnFunction.getNextImageIncorrect();
    },{once:true});
}

const incorrectQuizNextBtn = document.getElementById('incorrectQuizNextBtn');
if (incorrectQuizNextBtn !== null){
    incorrectQuizNextBtn.addEventListener('click', function () {
        func2();
    },false);
}
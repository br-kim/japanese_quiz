let btnFunction = {

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
            this.scoreAdd('correct');
            this.getNextImage();
        } else {
            alert("오답입니다!");
            this.scoreAdd('incorrect');
            table = document.getElementById('incorrect-sheet-table');
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
        new_url = await fetch("../quiz/new");
        data = new_url.text();
        json = JSON.parse(await data);
        url = json["path"];
        document.getElementById('quiz').src = url;
        document.getElementById('contain-answer').title = urlToFileName(url);
        this.answerClear();
    },

    toggleFunc : function () {
        target = document.getElementById('incorrect-sheet-table');
        if (target.style.visibility === "hidden") {
            target.style.visibility = "visible";
            document.getElementById('toggleBtn').innerText = "접기";
        } else {
            target.style.visibility = "hidden";
            document.getElementById('toggleBtn').innerText = "펼치기";
        }
    },

    getTableData : function () {
        table = document.getElementById('incorrect-sheet-table');
        arr = [];
        for (let i = 0; i < table.rows.length; i += 2) {
            buffer = Array.from(table.rows[i].cells);
            buffer.forEach(function (elem) {
                html = elem.innerHTML;
                arr.push(html);
            });
        }
        data = {chars: arr};
        return data;
    },

    requestQuizData : async function (kind) {
        let url = new URL('../quizdata','http://'+window.location.host);
        let tdata= this.getTableData();
        if(kind === true){
            url.search = new URLSearchParams(tdata).toString();
        }
        let r = await fetch(url);
        let j = await r.json();
        return j['order'];
    },

    getNextImage : async function () {
        let arrayNum = 0;
        let chars = await this.requestQuizData(false);
        console.log(arrayNum);
        document.getElementById("quiz").src = chars[arrayNum];
        document.getElementById('contain-answer').title = urlToFileName(chars[arrayNum]);
        return function () {
            arrayNum += 1;
            if (arrayNum < chars.length) {
                document.getElementById("quiz").src = chars[arrayNum];
                document.getElementById('contain-answer').title = urlToFileName(chars[arrayNum]);
            } else {
                document.getElementById('contain-answer').innerHTML = "퀴즈 종료.";
            }
            btnFunction.answerClear();
        };
    },

    getNextImageIncorrect : async function () {
        let arrayNum = 0;
        let chars = await this.requestQuizData(true);
        console.log(arrayNum);
        document.getElementById("quiz").src = chars[arrayNum];
        document.getElementById('contain-answer').title = urlToFileName(chars[arrayNum]);
        return function () {
            console.log("inner function");
            arrayNum += 1;
            if (arrayNum < chars.length) {
                document.getElementById("quiz").src = chars[arrayNum];
                document.getElementById('contain-answer').title = urlToFileName(chars[arrayNum]);
            } else {
                document.getElementById('contain-answer').innerHTML = "퀴즈 종료.";
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
        func1 = await btnFunction.getNextImage()
    })();
    getNextImageBtn.addEventListener('click', async () => {
        func1();
    }, false);
}

const incorrectQuizBtn = document.getElementById('incorrect-quizBtn');
if (incorrectQuizBtn !== null){
    incorrectQuizBtn.addEventListener('click',async () => {
        await (async () => {
            func2 = await btnFunction.getNextImageIncorrect();
        })();
    },{once:true});
    incorrectQuizBtn.addEventListener('click',async () =>{
        func2();
    },false);
}
function isCorrect(){
    answer = document.getElementById('answer').value;
    quiz = document.getElementById('contain-answer').title;
    if(answer === quiz){
        alert("정답입니다!");
        score = document.getElementById('correct').innerText;
        score = Number(score) + 1;
        document.getElementById('correct').innerText = score;
        document.getElementsByClassName('getNextBtn')[0].click();
    }
    else{
        alert("오답입니다!");
        score = document.getElementById('incorrect').innerText;
        score = Number(score) + 1;
        document.getElementById('incorrect').innerText = score;
        table = document.getElementById('incorrect-sheet-table');
        CellList = [];
        begin = table.rows.length-2;
        cellsLength = table.rows[begin].cells.length;
        if (cellsLength > 4){
            f = Math.floor(cellsLength/4);
            begin += 2*f;
            table.insertRow();
            table.insertRow();
        }

        for(let i = begin; i < begin+2; i++){
            CellList.push(table.rows[i].insertCell(-1));
        }
        CellList[0].innerHTML =
            "<img alt='image' src=" + document.getElementById('quiz').src + ">";

        CellList[1].innerText =
                document.getElementById('contain-answer').title;
    }
}

function showAnswer(){
    document.getElementById('show-answer').innerText = "정답은 " +
        document.getElementById('contain-answer').title + "입니다.";
}

function answerClear(){
    document.getElementById('answer').value = "";
    document.getElementById('show-answer').innerText = "";
}

async function getRandomImageUrl() {
    new_url = await fetch("../quiz/new");
    data = new_url.text();
    json = JSON.parse(await data);
    url = json["path"];
    document.getElementById('quiz').src = url;
    document.getElementById('contain-answer').title = urlToFileName(url);
    answerClear();
}

function toggleFunc(){
    target = document.getElementById('incorrect-sheet-table');
    if (target.style.visibility === "hidden"){
        target.style.visibility = "visible";
        document.getElementById('toggleBtn').innerText = "접기";
    } else{
        target.style.visibility = "hidden";
        document.getElementById('toggleBtn').innerText = "펼치기";
    }
}

function getTableData(){
    table = document.getElementById('incorrect-sheet-table');
    arr = [];
    for(let i = 0; i<table.rows.length; i+=2) {
        console.log(i);
        buffer = Array.from(table.rows[i].cells);
        buffer.forEach(function(elem){
            html = elem.innerHTML;
            arr.push(html);
        });
    }
    data = {chars : arr};
    return data;
}

requestQuizDataPost = async function (){
    let form = document.createElement('form');
    tdata = getTableData();
    form.method = "POST";
    form.action = "../incorrectquiz";
    let hiddenField = document.createElement('input');
    hiddenField.type = 'hidden';
    hiddenField.name = 'chars';
    hiddenField.value = JSON.stringify(tdata);
    form.appendChild(hiddenField);
    document.body.appendChild(form);
    form.submit();
};

requestQuizData = async function (reqMethod){
    tdata = getTableData();
    let r;
    if (reqMethod === "GET"){
        r = await fetch("../quizdata");
    }
    else{
        // r = await fetch("../quizdata", {
        //     method: "POST",
        //     body: JSON.stringify(tdata),
        // });
        requestQuizDataPost();
    }
    let j = await r.json();
    return j['order'];
};



var getNextImage = (async function (reqMethod) {
    arrayNum = 0;
    chars = await requestQuizData(reqMethod);
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
        answerClear();
    };
});


const submitBtn = document.getElementById('submitBtn');
if (submitBtn !== null){
    submitBtn.addEventListener('click',isCorrect,false);
}

const showAnswerBtn = document.getElementById('showAnswerBtn');
if (showAnswerBtn !== null){
    showAnswerBtn.addEventListener('click',showAnswer, false);
}
const getRandomImageBtn = document.getElementById('getRandomImageBtn');
if (getRandomImageBtn !== null) {
    getRandomImageBtn.addEventListener('click', getRandomImageUrl, false);
}
const toggleBtn = document.getElementById('toggleBtn');
if (toggleBtn !== null){
    toggleBtn.addEventListener('click',toggleFunc,false);
}

const getNextImageBtn = document.getElementById('getNextImageBtn');
if (getNextImageBtn !== null) {
    getNextImageBtn.addEventListener('click', async () => {
        let func = await getNextImage;
        func("GET");
    }, false);
}

const incorrectQuizBtn = document.getElementById('incorrect-quizBtn');
if (incorrectQuizBtn !== null){
    incorrectQuizBtn.addEventListener('click',async () => {
        let func = await getNextImage;
        func("POST");
    },false);

}
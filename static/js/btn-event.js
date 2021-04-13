function isCorrect(){
    answer = document.getElementById('answer').value;
    quiz = document.getElementById('contain-answer').title;
    if(answer === quiz){
        alert("정답입니다!");
        score = document.getElementById('correct').innerText;
        score = Number(score) + 1
        document.getElementById('correct').innerText = score;
    }
    else{
        alert("오답입니다!");
        score = document.getElementById('incorrect').innerText;
        score = Number(score) + 1
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
    new_url = await fetch("../quiz/new")
    data = new_url.text()
    json = JSON.parse(await data);
    url = json["path"]
    document.getElementById('quiz').src = url;
    document.getElementById('contain-answer').title = urlToFileName(url);
    answerClear();
}

function toggleFunc(){
    target = document.getElementById('incorrect-sheet-table');
    if (target.style.display === "none"){
        target.style.display = "block";
        document.getElementById('toggleButton').innerText = "접기";
    } else{
        target.style.display = "none"
        document.getElementById('toggleButton').innerText = "펼치기";
    }
}




const submitBtn = document.getElementById('submitBtn');
submitBtn.addEventListener('click',isCorrect,false);
const showAnswerBtn = document.getElementById('showAnswerBtn');
showAnswerBtn.addEventListener('click',showAnswer, false);
const getRandomImageBtn = document.getElementById('getRandomImageBtn');
getRandomImageBtn.addEventListener('click',getRandomImageUrl,false);
const toggleBtn = document.getElementById('toggleBtn');
toggleBtn.addEventListener('click',toggleFunc,false);


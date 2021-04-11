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

function urlToFileName(url){
    splited_url = url.split("/");
    result = splited_url[splited_url.length - 1].split(".")[0];
    return result;
}


function answerClear(){
    document.getElementById('answer').value = "";
    document.getElementById('show-answer').innerText = "";
}
let articleFunction = {
    sendArticle : async function (){
        let data = {
            title: document.getElementById('input-title').value,
            contents: document.getElementById('input-content').value
        };
        if (!data.title || !data.contents){
            alert('제목과 내용을 입력해주세요.');
            return;
        }
        res = await fetch('/freeboard/write/article',{
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        article_num = await res.text();
        window.location.href = location.origin + '/article?pagenum='+article_num;
    },

    editArticle : async function (){
        let urlSearchParams = new URLSearchParams(window.location.search);
        let params = Object.fromEntries(urlSearchParams.entries());
        let articleId = params.pagenum;
        let data = {
            title: document.getElementById('input-title').value,
            contents: document.getElementById('input-content').value
        };
        if (!data.title || !data.contents){
            alert('제목과 내용을 입력해주세요.');
            return;
        }
        res = await fetch(`/freeboard/edit/article/${articleId}`,{
            method:'PATCH',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        window.location.href = location.origin + '/article?pagenum='+articleId;
    },

    loadEdit : async ()=>{
        let urlSearchParams = new URLSearchParams(window.location.search);
        let params = Object.fromEntries(urlSearchParams.entries());
        let articleId = params.pagenum;
        location.href = `/article/edit?pagenum=${articleId}`

    },

    loadBeforeArticle : async ()=>{
        let urlSearchParams1 = new URLSearchParams(window.location.search);
        let params1 = Object.fromEntries(urlSearchParams1.entries());
        let res1 = await fetch(location.origin+'/freeboard/'+params1.pagenum);
        let article = await res1.json();
        console.log(article)
        document.getElementById('input-title').value = article.title
        document.getElementById('input-content').value = article.contents
    },

    loadArticle : async () => {
        let urlSearchParams = new URLSearchParams(window.location.search);
        let params = Object.fromEntries(urlSearchParams.entries());
        let res = await fetch(location.origin+'/freeboard/'+params.pagenum);
        let article = await res.json();
        document.getElementById('article-title').innerText = article.title;
        document.getElementById('article-content').innerText = article.contents;
        document.getElementById('article-writer').innerText = article.writer;
        document.getElementById('article-created').innerText = article.created_at.split('.')[0];
    },

    toggleComment : (target) => {
        if (target.style.visibility === "visible") {
            target.style.visibility = "hidden";
        } else {
            target.style.visibility = "visible";
        }
        return null;
    },

    buildComment : (ele) => {
        let commentDiv = document.createElement('div');
        let writerDiv = document.createElement('div');
        let contentsDiv = document.createElement('div');
        let button = document.createElement('button');
        let editInput = document.createElement('input');
        let inputLabel = document.createElement('label');
        let editButton = document.createElement('input');
        let deleteButton = document.createElement('input');

        editButton.type = 'button';
        editButton.value = '등록';

        inputLabel.appendChild(editInput)
        inputLabel.appendChild(editButton)
        inputLabel.id = `comment-edit-label-${ele.id}`
        inputLabel.classList.add('input-label')

        editInput.id = `comment-edit-input-${ele.id}`
        editButton.id = `comment-edit-submit-${ele.id}`

        button.innerText = '수정'
        deleteButton.type = 'button';
        deleteButton.value = '삭제';
        commentDiv.classList.add('contain-comment')
        writerDiv.id = 'comment-writer'
        contentsDiv.id = 'comment-contents'
        button.id = `comment-edit-button-${ele.id}`

        writerDiv.innerText += ele.writer
        contentsDiv.innerText += ele.contents
        commentDiv.appendChild(writerDiv)
        commentDiv.appendChild(button)
        commentDiv.appendChild(contentsDiv)
        commentDiv.appendChild(inputLabel)
        commentDiv.innerHTML += '<br>'
        document.getElementById('show-comments').appendChild(commentDiv)
        document.getElementById(`comment-edit-button-${ele.id}`)
            .addEventListener('click',()=>{
                articleFunction.toggleComment(document.getElementById(inputLabel.id))
            },false)
        document.getElementById(button.id).classList.add('comment-edit-button')
        document.getElementById(editButton.id).addEventListener(
            'click', ()=>{
                articleFunction.sendEditComment(document.getElementById(editInput.id));
            },false);
    },


    loadComments : async () => {
        urlSearchParams = new URLSearchParams(window.location.search);
        params = Object.fromEntries(urlSearchParams.entries());
        res = await fetch(location.origin+'/freeboard/'+params.pagenum+'/comment');
        comments = await res.json()
        comments.forEach(ele => {
            articleFunction.buildComment(ele);
        })
    },

    sendEditComment : async (elem) =>{
        urlSearchParams = new URLSearchParams(window.location.search);
        params = Object.fromEntries(urlSearchParams.entries());
        let commentId = elem.id.split("-")[elem.id.split("-").length-1];
        console.log(elem.id.split("-"))
        data = {
            contents: elem.value,
            article_id: Number(params.pagenum)
        };

        console.log(data);
        if (!data.article_id || !data.contents){
            alert('내용을 입력해주세요.')
            return
        }
        res = await fetch(`/freeboard/edit/comment/${commentId}`,{
            method:'PATCH',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
        window.location.href = location.origin + '/article?pagenum='+params.pagenum
    },

    sendComment : async () => {
        urlSearchParams = new URLSearchParams(window.location.search);
        params = Object.fromEntries(urlSearchParams.entries());

        data = {
            contents: document.getElementById('comment-contents').value,
            article_id: Number(params.pagenum)
        };
        console.log(data);
        if (!data.article_id || !data.contents){
            alert('내용을 입력해주세요.')
            return
        }
        res = await fetch('/freeboard/write/comment',{
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
        window.location.href = location.origin + '/article?pagenum='+params.pagenum
    }
};

let articleFunction = {
    getSearchParam: () => {
        let urlSearchParams = new URLSearchParams(window.location.search);
        return Object.fromEntries(urlSearchParams.entries());
    },

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
        let params = articleFunction.getSearchParam();
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
        let params = articleFunction.getSearchParam();
        let articleId = params.pagenum;
        location.href = `/article/edit?pagenum=${articleId}`;
    },

    loadBeforeArticle : async ()=>{
        let params = articleFunction.getSearchParam();
        let res = await fetch(location.origin+'/freeboard/'+params.pagenum);
        let article = await res.json();
        document.getElementById('input-title').value = article.title;
        document.getElementById('input-content').value = article.contents;
    },

    loadArticle : async () => {
        let params = articleFunction.getSearchParam();
        let res = await fetch(location.origin+'/freeboard/'+params.pagenum);
        let article = await res.json();
        document.title = article.title;
        document.getElementById('article-title').innerText = article.title;
        document.getElementById('article-content').innerText = article.contents;
        document.getElementById('article-writer').innerText = article.writer;
        let date = new Date(article.created_at);
        document.getElementById('article-created').innerText = date.toLocaleString("jpn",{dateStyle:'medium', timeStyle:'medium', hour12:false});
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
        let editSubmitButton = document.createElement('input');
        let deleteButton = document.createElement('input');

        editSubmitButton.type = 'button';
        editSubmitButton.value = '등록';

        inputLabel.appendChild(editInput);
        inputLabel.appendChild(editSubmitButton);
        inputLabel.id = `comment-edit-label-${ele.id}`;
        inputLabel.classList.add('input-label');

        editInput.id = `comment-edit-input-${ele.id}`;
        editSubmitButton.id = `comment-edit-submit-${ele.id}`;

        commentDiv.dataset.commentId = ele.id;


        button.innerText = '수정';
        deleteButton.type = 'button';
        deleteButton.value = '삭제';
        deleteButton.id = `comment-delete-button-${ele.id}`;
        commentDiv.classList.add('contain-comment');
        writerDiv.id = 'comment-writer';
        contentsDiv.id = 'comment-contents';
        button.id = `comment-edit-button-${ele.id}`;

        writerDiv.innerText += ele.writer;
        contentsDiv.innerText += ele.contents;
        commentDiv.appendChild(writerDiv);
        commentDiv.appendChild(button);
        commentDiv.appendChild(deleteButton);
        commentDiv.appendChild(contentsDiv);
        commentDiv.appendChild(inputLabel);
        commentDiv.innerHTML += '<br>';
        document.getElementById('show-comments').appendChild(commentDiv);
        document.getElementById(`comment-edit-button-${ele.id}`)
            .addEventListener('click',()=>{
                articleFunction.toggleComment(document.getElementById(inputLabel.id))
            },false);
        document.getElementById(button.id).classList.add('comment-edit-button');
        document.getElementById(editSubmitButton.id).addEventListener(
            'click', ()=>{
                articleFunction.sendEditComment(document.getElementById(editInput.id));
            },false);
        document.getElementById(deleteButton.id).classList.add('comment-edit-button');
        document.getElementById(deleteButton.id).addEventListener('click',async () =>{
            articleFunction.deleteComment(ele.id);
        }, false);
    },

    loadComments : async () => {
        params = articleFunction.getSearchParam();
        res = await fetch(location.origin+'/freeboard/'+params.pagenum+'/comment');
        comments = await res.json()
        comments.forEach(ele => {
            articleFunction.buildComment(ele);
        })
    },

    sendEditComment : async (elem) =>{
        params = articleFunction.getSearchParam();
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
        params = articleFunction.getSearchParam();
        data = {
            contents: document.getElementById('comment-contents').value,
            article_id: Number(params.pagenum)
        };
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
    },

    deleteArticle: async () => {
        let data = {
            content_id: Number(articleFunction.getSearchParam().pagenum)
        }
        await fetch(`/freeboard/delete/article`,{
            method:'DELETE',
            body: JSON.stringify(data)
        })
        window.location.href = document.referrer;
    },

    deleteComment: async (commentId) =>{
        let data = {
            content_id: commentId
        }
        await fetch('/freeboard/delete/comment',{
            method:'DELETE',
            body: JSON.stringify(data)
        })
        window.location.reload();
    },

    loadArticleList : async () => {
        let params = articleFunction.getSearchParam();
        let pagenum = params.page
        if (!pagenum){
            pagenum = 1
        }
        let url = new URL(location.origin + '/freeboard'+ '?/page='+pagenum);
        let data = {'page': pagenum};
        url.search = new URLSearchParams(data).toString();
        let req = await fetch(url);
        let res_json = await req.json();
        articleFunction.buildArticleHead(res_json.articles);
        articleFunction.buildPageIndex(res_json.articles_length,pagenum);
    },

    buildArticleHead : (articleJsonArray) => {
        document.getElementById('result').getElementsByTagName('tbody')[0].innerHTML = "";
        articleJsonArray.forEach(elem => {
            let newRow = document.getElementById('result').getElementsByTagName('tbody')[0].insertRow();
            let titleCell = newRow.insertCell();
            let writerCell = newRow.insertCell();
            let dateCell = newRow.insertCell();
            titleCell.innerHTML = `<a href="/article?pagenum=${elem.id}">${elem.title}</a>`;
            writerCell.textContent = elem.writer;
            let date = new Date(elem.created_at)
            dateCell.textContent = date.toLocaleString("jpn",{dateStyle:'medium', timeStyle:'medium', hour12:false});
        })
    },

    buildPageIndex: (totalPage,nowPage) => {
        document.getElementById('pages').innerHTML ="";
        for(let i = 1; i < totalPage+2; i++){
            document.getElementById('pages').innerHTML +=
                `<a href='/fb?page=${i}'>${i}</a> `;
        }
    }
};

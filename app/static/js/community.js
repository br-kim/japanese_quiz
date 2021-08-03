let articleFunction = {
    getSearchParamPagenum: () => {
        let urlSearchParams = new URLSearchParams(window.location.search);
        let result = Object.fromEntries(urlSearchParams.entries());
        return result.pagenum;
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
        let res = await fetch('/freeboard/write/article',{
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        let article_num = await res.text();
        window.location.href = location.origin + '/article?pagenum='+article_num;
    },

    editArticle : async function (){
        let articleId = articleFunction.getSearchParamPagenum();
        let data = {
            title: document.getElementById('input-title').value,
            contents: document.getElementById('input-content').value
        };
        if (!data.title || !data.contents){
            alert('제목과 내용을 입력해주세요.');
            return;
        }
        await fetch(`/freeboard/edit/article/${articleId}`,{
            method:'PATCH',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        window.location.href = location.origin + '/article?pagenum='+articleId;
    },

    loadEdit : async ()=>{
        let articleId = articleFunction.getSearchParamPagenum();
        location.href = `/article/edit?pagenum=${articleId}`;
    },

    loadBeforeArticle : async ()=>{
        let res = await fetch(location.origin+'/freeboard/'+articleFunction.getSearchParamPagenum());
        let article = await res.json();
        document.getElementById('input-title').value = article.title;
        document.getElementById('input-content').value = article.contents;
    },

    loadArticle : async () => {
        let res = await fetch(location.origin+'/freeboard/'+articleFunction.getSearchParamPagenum());
        let article = await res.json();
        /** @param article
         *  @param article.title
         *  @param article.contents
         *  @param article.writer
         *  @param article.created_at
         */
        document.title = article.title;
        document.getElementById('article-title').innerText = article.title;
        document.getElementById('article-content').innerText = article.contents;
        document.getElementById('article-writer').innerText = article.writer;
        let date = new Date(article.created_at);
        document.getElementById('article-created').innerText =
            date.toLocaleString("jpn",{dateStyle:'medium', timeStyle:'medium', hour12:false});
    },

    toggleComment : (target) => {
        if (target.style.visibility === "visible") {
            target.style.visibility = "hidden";
        } else {
            target.style.visibility = "visible";
        }
        return null;
    },

    buildCommentEdit : (ele) => {
        let inputLabel = document.createElement('label');
        let editInput = document.createElement('input');
        let editSubmitButton = document.createElement('input');
        editSubmitButton.type = 'button';
        editSubmitButton.value = '등록';
        inputLabel.appendChild(editInput);
        inputLabel.appendChild(editSubmitButton);
        inputLabel.id = `comment-edit-label-${ele.id}`;
        inputLabel.classList.add('input-label');
        editInput.id = `comment-edit-input-${ele.id}`;
        editSubmitButton.id = `comment-edit-submit-${ele.id}`;

        return inputLabel;
    },

    buildComment : (comment) => {
        let commentDiv = document.createElement('div');
        let writerDiv = document.createElement('div');
        let contentsDiv = document.createElement('div');
        let editButton = document.createElement('button');
        let deleteButton = document.createElement('input');
        let createAtDiv = document.createElement('div');

        editButton.innerText = '수정';
        editButton.id = `comment-edit-button-${comment.id}`;

        deleteButton.type = 'button';
        deleteButton.value = '삭제';
        deleteButton.id = `comment-delete-button-${comment.id}`;

        commentDiv.dataset.commentId = comment.id;
        commentDiv.classList.add('contain-comment');
        writerDiv.id = 'comment-writer';
        contentsDiv.id = 'comment-contents';
        createAtDiv.id = 'comment-created-at';
        writerDiv.innerText += comment.writer;
        contentsDiv.innerText += comment.contents;
        let date = new Date(comment.created_at);
        createAtDiv.innerText += date.toLocaleString("jpn",{dateStyle:'medium', timeStyle:'medium', hour12:false});

        let inputLabel = articleFunction.buildCommentEdit(comment);

        commentDiv.appendChild(writerDiv);
        commentDiv.appendChild(createAtDiv);
        commentDiv.innerHTML += '<br>';

        commentDiv.appendChild(editButton);
        commentDiv.appendChild(deleteButton);
        commentDiv.appendChild(contentsDiv);
        commentDiv.innerHTML += '<br>';
        commentDiv.appendChild(inputLabel);
        commentDiv.innerHTML += '<br>';
        commentDiv.innerHTML += '<br>';

        document.getElementById('show-comments').appendChild(commentDiv);
        document.getElementById(editButton.id).classList.add('comment-edit-button');
        document.getElementById(`comment-edit-button-${comment.id}`)
            .addEventListener('click',()=>{
                articleFunction.toggleComment(document.getElementById(`comment-edit-label-${comment.id}`));
            },false);
        document.getElementById(`comment-edit-submit-${comment.id}`).addEventListener(
            'click', async ()=>{
                console.log(comment.id);
                await articleFunction.sendEditComment(document.getElementById(`comment-edit-input-${comment.id}`));
            },false);
        document.getElementById(deleteButton.id).classList.add('comment-edit-button');
        document.getElementById(deleteButton.id).addEventListener('click',async () =>{
            await articleFunction.deleteComment(comment);
        }, false);
    },

    loadComments : async () => {
        let res = await fetch(location.origin+'/freeboard/'+articleFunction.getSearchParamPagenum()+'/comment');
        let comments = await res.json();
        comments.forEach(comment => {
            articleFunction.buildComment(comment);
        });
    },

    sendEditComment : async (elem) =>{
        let pagenum = articleFunction.getSearchParamPagenum();
        let commentId = elem.id.split("-")[elem.id.split("-").length-1];
        console.log(elem.id.split("-"));
        let data = {
            contents: elem.value,
            article_id: Number(pagenum)
        };

        console.log(data);
        if (!data.article_id || !data.contents){
            alert('내용을 입력해주세요.');
            return;
        }
        await fetch(`/freeboard/edit/comment/${commentId}`,{
            method:'PATCH',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        window.location.href = location.origin + '/article?pagenum='+pagenum;
    },

    sendComment : async () => {
        let pagenum = articleFunction.getSearchParamPagenum();
        let data = {
            contents: document.getElementById('write-comment-input').value,
            article_id: Number(pagenum)
        };
        if (!data.article_id || !data.contents){
            alert('내용을 입력해주세요.');
            return;
        }
        await fetch('/freeboard/write/comment',{
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        window.location.href = location.origin + '/article?pagenum='+pagenum;
    },

    deleteArticle: async () => {
        let data = {
            content_id: Number(articleFunction.getSearchParamPagenum()),
            content_writer: document.getElementById('article-writer')
        };
        await fetch(`/freeboard/delete/article`,{
            method:'DELETE',
            body: JSON.stringify(data)
        });
        window.location.href = document.referrer;
    },

    deleteComment: async (comment) =>{
        let data = {
            content_id: comment.id,
            content_writer: comment.writer
        };
        await fetch('/freeboard/delete/comment',{
            method:'DELETE',
            body: JSON.stringify(data)
        });
        window.location.reload();
    },
    loadArticleList : async () => {
        let pagenum =  articleFunction.getSearchParamPagenum();
        if (!pagenum){
            pagenum = 1;
        }
        let url = new URL(location.origin + '/freeboard'+ '?/pagenum='+pagenum);
        let data = {'page': pagenum};
        url.search = new URLSearchParams(data).toString();
        let req = await fetch(url.toString());
        let res_json = await req.json();
        /** @param res_json
         *  @param res_json.articles
         *  @param res_json.articles_length
         *  **/
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
            let date = new Date(elem.created_at);
            dateCell.textContent = date.toLocaleString("jpn",{dateStyle:'medium', timeStyle:'medium', hour12:false});
        });
    },

    buildPageIndex: (totalPage) => {
        document.getElementById('pages').innerHTML ="";
        for(let i = 1; i < totalPage+2; i++){
            document.getElementById('pages').innerHTML +=
                `<a href='/fb?pagenum=${i}'>${i}</a> `;
        }
    }
};

let articleFunction = {
    datePreProcess: (timeStamp) =>{
        let date = new Date(timeStamp);
        return date.toLocaleString("jpn", {dateStyle: 'medium', timeStyle: 'medium', hour12: false});
    },

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
            headers : btnFunction.tokenHeader,
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
            headers : btnFunction.tokenHeader,
            body: JSON.stringify(data)
        }).then(res=>{
            if(res.status === 403){
                alert("다른 사람의 글은 수정할 수 없습니다.");
            }});
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
        document.getElementById('article-created').innerText =
            articleFunction.datePreProcess(article.created_at);
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
        let createAtDiv = document.createElement('div');

        let editButton = document.createElement('button');
        let deleteButton = document.createElement('input');
        let childCommentButton = document.createElement('input');

        childCommentButton.type = 'button';
        childCommentButton.value = '대댓글';
        childCommentButton.id = `child-comment-button-${comment.id}`;

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
        createAtDiv.innerText += articleFunction.datePreProcess(comment.created_at);

        let inputLabel = articleFunction.buildCommentEdit(comment);
        childCommentButton.classList.add('comment-edit-button');
        editButton.classList.add('comment-edit-button');
        deleteButton.classList.add('comment-edit-button');

        commentDiv.append(writerDiv, createAtDiv);
        commentDiv.innerHTML += '<br>';
        commentDiv.append(editButton, deleteButton);
        if(comment.id === comment.parent_id) {
            commentDiv.append(childCommentButton);
        }
        commentDiv.appendChild(contentsDiv);
        commentDiv.innerHTML += '<br>';
        commentDiv.appendChild(inputLabel);
        commentDiv.innerHTML += '<br> <br>';

        document.getElementById('show-comments').appendChild(commentDiv);
        document.getElementById(`comment-edit-button-${comment.id}`)
            .addEventListener('click',()=>{
                articleFunction.toggleComment(document.getElementById(`comment-edit-label-${comment.id}`));
            },false);
        document.getElementById(`comment-edit-submit-${comment.id}`).addEventListener(
            'click', async ()=>{
                await articleFunction.sendEditComment(document.getElementById(`comment-edit-input-${comment.id}`));
            },false);
        if (document.getElementById(`child-comment-button-${comment.id}`)) {
            document.getElementById(`child-comment-button-${comment.id}`)
                .addEventListener("click", async () => {
                    articleFunction.changeChildComment(comment.id);
                });
        }
        document.getElementById(deleteButton.id).addEventListener('click',async () =>{
            await articleFunction.deleteComment(comment);
        }, false);
    },
    changeChildComment : (commentId) => {
        let state = document.getElementById("state-childcomment").value;
        let comment = document.querySelector(`[data-comment-id="${commentId}"]`);
        if (state === "true"){
            document.getElementById("state-childcomment").value = 'false';
            comment.classList.replace('contain-comment','selected-comment');
            const oriElement = document.getElementById('write-comment-submit');
            let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
            document.getElementById('write-comment-submit').replaceWith(cloneElement);
            document.getElementById('write-comment-submit')
                .addEventListener('click',()=> {
                    articleFunction.sendComment(commentId);
                    let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
                    // document.getElementById('write-comment-submit').replaceWith(cloneElement);
                    document.body.querySelector('#write-comment-submit').replaceWith(oriElement);
                });
        }else{
            document.getElementById("state-childcomment").value = 'true';
            comment.classList.replace('selected-comment','contain-comment');
            let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
            document.getElementById('write-comment-submit').replaceWith(cloneElement);
            document.getElementById("write-comment-submit").addEventListener('click',()=>{
                articleFunction.sendComment();
            });
        }
    },
    loadComments : async () => {
        let res = await fetch(location.origin+'/freeboard/'+articleFunction.getSearchParamPagenum()+'/comment');
        let comments = await res.json();
        comments.forEach((comment)=>{
            if (!comment.parent_id){
                comment.parent_id = comment.id;
            }else{
                comment.contents = "(대댓글)"+comment.contents ;
            }
        });
        comments.sort((a,b)=>{
            if(a.parent_id > b.parent_id) return 1;
            if(a.parent_id === b.parent_id) return a.id-b.id;
            if(a.parent_id < b.parent_id) return -1;
        });
        comments.forEach((comment)=>{
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
            headers : btnFunction.tokenHeader,
            body: JSON.stringify(data)
        }).then(res=>{
            if(res.status === 403){
                alert("다른 사람의 댓글은 수정할 수 없습니다.");
            }});
        window.location.href = location.origin + '/article?pagenum='+pagenum;
    },

    sendComment : async (parentId) => {
        let pagenum = articleFunction.getSearchParamPagenum();
        let data = {
            contents: document.getElementById('write-comment-input').value,
            article_id: Number(pagenum),
            parent_id: parentId
        };
        if (!data.article_id || !data.contents) {
            alert('내용을 입력해주세요.');
            return;
        }
        await fetch('/freeboard/write/comment', {
            method: 'POST',
            headers : btnFunction.tokenHeader,
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
            headers: btnFunction.tokenHeader,
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
            headers: btnFunction.tokenHeader,
            body: JSON.stringify(data)
        }).then(res=>{
            if(res.status === 403){
                alert("다른 사람의 댓글은 삭제할 수 없습니다.");
            }});
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
        articleJsonArray.forEach(elem => {
            let newRow = document.getElementById('result').getElementsByTagName('tbody')[0].insertRow();
            let titleCell = newRow.insertCell();
            let writerCell = newRow.insertCell();
            let dateCell = newRow.insertCell();
            titleCell.innerHTML = `<a href="/article?pagenum=${elem.id}">${elem.title}</a>`;
            writerCell.textContent = elem.writer;
            dateCell.textContent = articleFunction.datePreProcess(elem.created_at);
        });
    },

    buildPageIndex: (totalPage, nowPage=1) => {
        nowPage = Number(nowPage);
        let begin = nowPage;
        if (nowPage > 1){
            begin = nowPage-2;
            if(begin < 1){
                begin = 1;
            }
        }
        let end = begin+5;
        if (end > totalPage){
            end = totalPage;
        }
        document.getElementById('pages').innerHTML ="";
        for(let i = begin; i < end; i++){
            document.getElementById('pages').innerHTML +=
                `<a href='/fb?pagenum=${i}'>${i}</a> `;
        }
    }
};

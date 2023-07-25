import {requestToServer,} from "./index.js";
import {btnFunction} from "./btn-event.js";

export let articleFunction = {
    datePreProcess: (timeStamp) => {
        let date = new Date(timeStamp);
        let today = new Date();
        if (date.toLocaleDateString() === today.toLocaleDateString()) {
            return date.toLocaleTimeString("jpn", {hour: '2-digit', minute: '2-digit'});
        } else {
            return date.toLocaleDateString("jpn", {year: 'numeric', month: '2-digit', day: '2-digit'});
        }
    },

    getSearchParamPagenum: () => {
        let urlSearchParams = new URLSearchParams(window.location.search);
        let result = Object.fromEntries(urlSearchParams.entries());
        return result.pagenum;
    },

    getArticleIdFromURL: () => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const articleId = urlParams.get('article_id');
        return articleId;
    },
    sendArticle: async function () {
        let data = {
            title: document.getElementById('input-title').value,
            contents: document.getElementById('input-content').value
        };
        if (!data.title || !data.contents) {
            alert('제목과 내용을 입력해주세요.');
            return;
        }
        let res = await requestToServer(
            '/freeboard/write/article', "POST", true, JSON.stringify(data));
        let article_num = await res.text();
        window.location.href = location.origin + '/article?article_id=' + article_num;
    },
    editArticle: async function () {
        let articleId = articleFunction.getArticleIdFromURL();
        let data = {
            title: document.getElementById('input-title').value,
            contents: document.getElementById('input-content').value
        };
        if (!data.title || !data.contents) {
            alert('제목과 내용을 입력해주세요.');
            return;
        }
        let res = await requestToServer(
            `/freeboard/edit/article/${articleId}`, "PATCH", true, JSON.stringify(data));
        if (res.status === 403) {
            alert("다른 사람의 글은 수정할 수 없습니다.");
        }
        window.location.href = location.origin + '/article?article_id=' + articleId;
    },

    loadEdit: async () => {
        let articleId = articleFunction.getArticleIdFromURL();
        location.href = `/article/edit?article_id=${articleId}`;
    },

    loadBeforeArticle: async () => {
        let res = await requestToServer(
            location.origin + '/freeboard/' + articleFunction.getArticleIdFromURL(), "GET", true);
        let article = await res.json();
        document.getElementById('input-title').value = article.title;
        document.getElementById('input-content').value = article.contents;
    },

    loadArticle: async () => {
        let res = await requestToServer(
            location.origin + '/freeboard/' + articleFunction.getArticleIdFromURL(), "GET", true);
        let article = await res.json();
        /** @param article
         *  @param article.title
         *  @param article.contents
         *  @param article.writer
         *  @param article.created_at
         */
        document.title = article.title;
        // document.getElementById('article-title').innerText = article.title;
        document.getElementById('article-title').innerHTML = `<h3>${article.title}</h3>`;
        document.getElementById('article-content').innerText = article.contents;
        document.getElementById('article-writer').innerText = article.writer;
        document.getElementById('article-created').innerText =
            articleFunction.datePreProcess(article.created_at);
    },

    toggleComment: (target) => {
        // 댓글 수정 시 댓글 밑에 수정 항목이 보일지 말지 결정
        if (target.style.visibility === "visible") {
            target.style.visibility = "hidden";
        } else {
            target.style.visibility = "visible";
        }
        return null;
    },

    buildCommentEdit: (ele) => {
        let inputLabel = document.createElement('label');
        let editInput = document.createElement('input');
        let editSubmitButton = document.createElement('input');
        editSubmitButton.type = 'button';
        editSubmitButton.value = '등록';
        editSubmitButton.classList.add("btn", "btn-primary", "btn-sm");
        inputLabel.appendChild(editInput);
        inputLabel.appendChild(editSubmitButton);
        inputLabel.id = `comment-edit-label-${ele.id}`;
        inputLabel.classList.add('input-label');
        editInput.id = `comment-edit-input-${ele.id}`;
        editSubmitButton.id = `comment-edit-submit-${ele.id}`;

        return inputLabel;
    },

    buildComment: (comment) => {

        let commentDiv = document.createElement('div');

        let writerDiv = document.createElement('div');
        let contentsDiv = document.createElement('div');
        let createAtDiv = document.createElement('div');

        let editButton = document.createElement('button');
        let deleteButton = document.createElement('input');
        let childCommentButton = document.createElement('input');

        let buttonContainerDiv = document.createElement('div');
        let commentInfoDiv = document.createElement('div');
        let commentHeaderDiv = document.createElement('div');
        commentHeaderDiv.classList.add("d-flex", "justify-content-between");

        childCommentButton.type = 'button';
        childCommentButton.value = '대댓글';
        childCommentButton.id = `child-comment-button-${comment.id}`;
        childCommentButton.classList.add("btn", "btn-primary", "btn-sm");

        editButton.innerText = '수정';
        editButton.id = `comment-edit-button-${comment.id}`;
        editButton.classList.add("btn", "btn-secondary", "btn-sm");

        deleteButton.type = 'button';
        deleteButton.value = '삭제';
        deleteButton.id = `comment-delete-button-${comment.id}`;
        deleteButton.classList.add("btn", "btn-danger", "btn-sm");

        commentDiv.dataset.commentId = comment.id;
        commentDiv.classList.add('contain-comment');
        writerDiv.id = 'comment-writer';
        contentsDiv.id = 'comment-contents';
        createAtDiv.id = 'comment-created-at';
        writerDiv.innerText += comment.writer;
        contentsDiv.innerText += comment.contents;
        createAtDiv.innerText += articleFunction.datePreProcess(comment.created_at);

        let inputLabel = articleFunction.buildCommentEdit(comment);
        inputLabel.style.visibility = "hidden";

        commentInfoDiv.append(writerDiv, createAtDiv);
        commentHeaderDiv.append(commentInfoDiv, buttonContainerDiv);
        commentDiv.append(commentHeaderDiv);
        buttonContainerDiv.append(editButton, deleteButton);
        if (comment.id === comment.parent_id) {
            buttonContainerDiv.append(childCommentButton);
        }
        commentDiv.appendChild(contentsDiv);
        commentDiv.appendChild(inputLabel);
        commentDiv.innerHTML += '<hr>';
        if (comment.parent_id != comment.id) {
            commentDiv.classList.add("child-comment");
        }
        document.getElementById('show-comments').appendChild(commentDiv);
        document.getElementById(`comment-edit-button-${comment.id}`)
            .addEventListener('click', () => {
                articleFunction.toggleComment(document.getElementById(`comment-edit-label-${comment.id}`));
            });
        document.getElementById(`comment-edit-submit-${comment.id}`).addEventListener(
            'click', async () => {
                await articleFunction.sendEditComment(document.getElementById(`comment-edit-input-${comment.id}`));
            });
        if (document.getElementById(`child-comment-button-${comment.id}`)) {
            document.getElementById(`child-comment-button-${comment.id}`)
                .addEventListener("click", async () => {
                    articleFunction.changeChildComment(comment.id);
                });
        }
        document.getElementById(deleteButton.id).addEventListener('click', async () => {
            await articleFunction.deleteComment(comment);
        });
    },

    changeChildComment: (commentId) => {
        console.log("changeChildComment");
        let state = document.getElementById("state-childcomment").value;
        let comment = document.querySelector(`[data-comment-id="${commentId}"]`);
        console.log(comment);
        if (state === "true") {
            console.log("true");
            document.getElementById("state-childcomment").value = "false";
            comment.classList.replace('contain-comment', 'selected-comment');
            const oriElement = document.getElementById('write-comment-submit');
            let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
            document.getElementById('write-comment-submit').replaceWith(cloneElement);
            document.getElementById('write-comment-submit')
                .addEventListener('click', () => {
                    articleFunction.sendComment(commentId);
                    let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
                    // document.getElementById('write-comment-submit').replaceWith(cloneElement);
                    document.body.querySelector('#write-comment-submit').replaceWith(oriElement);
                });
        } else {
            document.getElementById("state-childcomment").value = "true";
            comment.classList.replace('selected-comment', 'contain-comment');
            let cloneElement = document.getElementById('write-comment-submit').cloneNode(true);
            document.getElementById('write-comment-submit').replaceWith(cloneElement);
            document.getElementById("write-comment-submit").addEventListener('click', () => {
                articleFunction.sendComment();
            });
        }
    },
    loadComments: async () => {
        let res = await requestToServer(
            location.origin + `/freeboard/${articleFunction.getArticleIdFromURL()}/comment`, 'GET', true);
        let comments = await res.json();
        comments.forEach((comment) => {
            if (!comment.parent_id) {
                comment.parent_id = comment.id;
            } else {
                comment.contents = "(대댓글)" + comment.contents;
            }
        });
        comments.sort((a, b) => {
            if (a.parent_id > b.parent_id) return 1;
            if (a.parent_id === b.parent_id) return a.id - b.id;
            if (a.parent_id < b.parent_id) return -1;
        });
        comments.forEach((comment) => {
            articleFunction.buildComment(comment);
        });
    },

    sendEditComment: async (elem) => {
        let articleId = articleFunction.getArticleIdFromURL();
        let commentId = elem.id.split("-")[elem.id.split("-").length - 1];
        let data = {
            contents: elem.value,
        };
        if (!data.contents) {
            alert('내용을 입력해주세요.');
            return;
        }
        let res = await requestToServer(
            `/freeboard/comment/${commentId}`, 'PATCH', true, JSON.stringify(data));
        if (res.status === 403) {
            alert("다른 사람의 댓글은 수정할 수 없습니다.");
        }
        window.location.href = location.origin + '/article?article_id=' + articleId;
    },

    sendComment: async (parentId) => {
        let articleId = articleFunction.getArticleIdFromURL();
        let data = {
            contents: document.getElementById('write-comment-input').value,
            article_id: Number(articleId),
            parent_id: parentId
        };
        if (!data.article_id || !data.contents) {
            alert('내용을 입력해주세요.');
            return;
        }
        await requestToServer('/freeboard/write/comment', 'POST', true, JSON.stringify(data));
        window.location.href = location.origin + '/article?article_id=' + articleId;
    },

    deleteArticle: async () => {
        let article_id = articleFunction.getArticleIdFromURL();
        let url = new URL(location.origin + `/freeboard/article/${article_id}`);
        let res = await requestToServer(
            url, 'DELETE', true);
        window.location.href = document.referrer;
    },

    deleteComment: async (comment) => {
        let res = await requestToServer(`/freeboard/comment/${comment.id}`,
            'DELETE', true);
        if (res.status === 403) {
            alert("다른 사람의 댓글은 삭제할 수 없습니다.");
        }
        window.location.reload();
    },

    loadArticleList: async () => {
        let pageNum = articleFunction.getSearchParamPagenum();
        if (!pageNum) {
            pageNum = 1;
        }
        let url = new URL(location.origin + '/freeboard' + '?/pagenum=' + pageNum);
        let data = {'page': pageNum};
        url.search = new URLSearchParams(data).toString();
        let req = await requestToServer(url.toString(), "GET");
        let res_json = await req.json();
        /** @param res_json
         *  @param res_json.articles
         *  @param res_json.articles_length
         *  **/
        articleFunction.buildArticleHead(res_json.articles);
        articleFunction.buildPageIndex(res_json.articles_length, pageNum);
    },

    buildArticleHead: (articleJsonArray) => {
        articleJsonArray.forEach(elem => {
            let newRow = document.getElementById('result').getElementsByTagName('tbody')[0].insertRow();
            let titleCell = newRow.insertCell();
            let writerCell = newRow.insertCell();
            let dateCell = newRow.insertCell();
            titleCell.innerHTML = `<a href="/article?article_id=${elem.id}">${elem.title}</a>`;
            writerCell.textContent = elem.writer;
            dateCell.textContent = articleFunction.datePreProcess(elem.created_at);
        });
    },

    buildPageIndex: (totalPage, nowPage = 1) => {
        nowPage = Number(nowPage);
        let div = Math.floor(nowPage / 5);
        let mod = nowPage % 5;
        if (mod === 0) {
            div -= 1;
        }
        let begin = (div * 5) + 1;
        let end = ((div + 1) * 5) + 1;
        if (end > totalPage) {
            end = totalPage + 1;
        }
        let pageList = document.getElementById('page-list');
        if (div > 0) {
            pageList.innerHTML +=
                `<li class="page-item" ><a class="page-link" href="/fb?pagenum=${begin - 1}">이전</a></li>`;
        }
        for (let i = begin; i < end; i++) {
            pageList.innerHTML +=
                `<li class="page-item" ><a class="page-link" href="/fb?pagenum=${i}">${i}</a></li>`;
        }
        if (end !== totalPage + 1) {
            pageList.innerHTML +=
                `<li class="page-item" ><a class="page-link" href="/fb?pagenum=${end}">다음</a></li>`;
        }
    }
};

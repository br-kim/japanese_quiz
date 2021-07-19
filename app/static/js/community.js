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
    }
};

function search(){
    let textToSearch = document.getElementById("text-to-search").value;
    let paragraph = document.getElementById("paragraph");
    textToSearch = textToSearch.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");

    let pattern = new RegExp(`${textToSearch}`,"gi");
    
    paragraph.innerHTML = paragraph.textContent.replace(pattern, match => `<mark>${match}</mark>`)
}

function searcharea(){
    let textToSearch = document.getElementById("text-to-search").value;
    let paragraph = document.getElementById("form7");
    textToSearch = textToSearch.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");

    let pattern = new RegExp(`${textToSearch}`,"gi");

    paragraph.innerHTML = paragraph.value.replace(pattern, match => `<mark>${match}</mark>`);

    console.log(textToSearch);
    console.log(paragraph);
}
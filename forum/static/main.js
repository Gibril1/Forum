const addButton = document.getElementById('add');
// const post = document.getElementById('post')

addButton.addEventListener('click', ()=>{
    console.log('clicked');
    const input = document.createElement('textarea');
    input.setAttribute('name','comment');
    input.classList.add('textarea');
    const submit = document.createElement('button');
    submit.innerHTML = 'Post Comment'
    submit.classList.add('btn-primary');

    post.appendChild(input);
    post.appendChild(submit);
})
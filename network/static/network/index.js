document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#publish").addEventListener('click', event => publish_post(event));
    loadPosts('all');
    console.log('page loaded!');
});

function loadPosts(type="all") {

    fetch(`posts/${type}`)
    .then((response) => response.json())
    .then((posts) => {
        posts.forEach((post) =>{
            renderPost(post);
        });
    });
}

function renderPost(post) {
    const content = document.createElement("div");
    // console.log(post);
    content.innerHTML = `
  <div class="post-author">
    <a href="/profile/${post.author}">${post.author}</a>
    </div>
  <div class="post-body">${post.body}</div>
  <div class="post-timestamp">${post.timestamp}</div>
  `;

  document.querySelector('#js').append(content);
}


function publish_post(event) {
	event.preventDefault(); // prevents form submission reloading current page

	fetch("/posts", {
		method: "POST",
		body: JSON.stringify({
			body: document.querySelector("#post-body").value
		}),})
		.then((response) => response.json())
		.then((result) => {
			console.log(result);
            loadPosts();
	});

}
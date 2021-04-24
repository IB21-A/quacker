document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector("body").dataset.title == "index") {
        document.querySelector("#publish").addEventListener('click', event => publishPost(event));
        loadPosts('all');
        console.log('page loaded!');
        document.querySelectorAll(".heart").forEach(function(item) {
            item.onclick = function() {
                postId = item.dataset.postid;
                toggleLike(postId);
            }
        });
        // add eventlistener to hearts
        // make clicking a heart log something on console
        // make clicking a heart call the API to toggle like
        
    }

    if (document.querySelector("body").dataset.title == "profile") {
        console.log('do profile stuff');
        document.querySelector("#btn-follow").addEventListener('click', event => toggleFollow(event));
    }
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

    // <div class="post-wrapper">
    // <div class="post-profile-photo"><img src="{% static 'network/img/ducky_icon.gif' %}" alt="Profile Photo"></div>
    // <div class="post-content">
    //     <a href="{%url 'profile' post.author.username %}">{{ post.author }}</a> says {{ post.body }} on {{ post.timestamp }}
    //     <div class="heart"><i class="fas fa-heart"><i class="far fa-heart"></i></i></div>
    // </div>
    // </div>

  document.querySelector('#js').append(content);
}


function publishPost(event) {
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

function toggleFollow(event) {
    event.preventDefault();

    username = document.querySelector("#username").innerHTML;
    fetch(`/follow/${username}`, {
        method: 'PUT'})
        .then(
            response => response.json()
        )
        .then(status => {
            console.log(status);
            updateFollowButton(status);
            // Display a toast?
        });
}

function updateFollowButton(status) {
    followButton = document.querySelector('#btn-follow');
    if (status.following === true) {
        followButton.classList.add('btn-secondary');
        followButton.classList.remove('btn-primary');
        followButton.innerHTML = 'Unfollow';
        return;
    }

    followButton.innerHTML = 'Follow';
    followButton.classList.add('btn-primary');
    followButton.classList.remove('btn-secondary');
    return;
}

function toggleLike(postId) {
    fetch(`/posts/like/${postId}`, {
        method: 'PUT'})
        .then(response => response.json())
        .then(status => {
            updateLikeButton(postId, status)
        });
}

function updateLikeButton(postId, status) {
    likeButton = document.querySelector(`[data-postid="${postId}"]`);
    if (status.liked === true) {
        likeButton.innerHTML = '<i class="fas fa-heart"></i>';
        return;
    }

    likeButton.innerHTML = '<i class="far fa-heart"></i>';
    return;
}
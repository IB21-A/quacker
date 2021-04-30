document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector("body").dataset.title == "index") {
        document.querySelector("#publish").addEventListener('click', event => publishPost(event));
        // loadPosts('all');
        console.log('page loaded!');
        
        addButtonListeners();
        
        
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

//   document.querySelector('#js').append(content);
}

function addButtonListeners() {
    document.querySelectorAll(".post-wrapper").forEach(item => {
        let postId = item.dataset.postid;

        let heart = item.querySelector(".heart");
        heart.onclick = function() {
            toggleLike(postId);
        };

        let options = item.querySelector(".post-options");
        if (options != null) {
            let editButton = options.querySelector(".post-edit");
            editButton.onclick = function() {

                closeEditPosts(); // Close any open post editors

                postBody = item.querySelector(".post-body");
                postEditSpace = item.querySelector(".post-body-edit");
                postBodyContent = postBody.innerHTML;
                postBody.style.display = "none";
                
                
                let editPostForm = createEditPostForm();
                input = editPostForm.querySelector('#edit-input');
                input.value = postBodyContent;

                // Hide edit button
                editButton.style.display = "none";

                
                // add form to body
                postEditSpace.appendChild(editPostForm);

                console.log(postBodyContent);
                // create an edit text box
                // fill it with existing post content
            };
        }
    });
}

function createEditPostForm() {
    let form = document.createElement('form');
    let formInput = document.createElement('textarea');
    let cancelButton = document.createElement('span');
    let submitButton = document.createElement('span');
    form.appendChild(formInput);
    form.className = 'post-form';
    form.id = 'edit-post-form'
    formInput.className = 'form-control';
    formInput.id = 'edit-input';
    cancelButton.className = 'btn btn-sm btn-secondary post-form-button';
    cancelButton.innerText = 'Cancel';
    submitButton.className = 'btn btn-sm btn-primary post-form-button';
    submitButton.innerText = 'Submit';
    form.appendChild(cancelButton);
    form.appendChild(submitButton);

    cancelButton.onclick = closeEditPosts; // I need to bypass the regular behavior of a button here
    submitButton.onclick = submitEditPost;

    return form;
}

function closeEditPosts() {
    // Selecting all to ensure no more than 1 can be open at a time
    document.querySelectorAll('#edit-post-form').forEach(form => {
        post = form.closest('.post-wrapper');
        postOptions = post.querySelector('.post-edit');
        postBody = post.querySelector('.post-body');

        // Unhide post body and edit button
        postBody.style.display = 'block';
        postOptions.style.display = 'block';

        form.remove();
    }); 
    

}

function submitEditPost() {
    form = document.querySelector('#edit-post-form');
    post = form.closest('.post-wrapper');
    postId = post.dataset.postid;
    
    fetch(`/posts/edit/${postId}`, {
            method: "PUT",
            body: JSON.stringify({
                body: post.querySelector('#edit-input').value
            })
        })
        .then(response => response.json())
        .then(result => {
            if ('error' in result){
                return alert(result.error);
            }

            console.log(result);
            updatePostFromEdit(post, result);
            closeEditPosts();
        });

    
    
}

function updatePostFromEdit(post, result){
    postBody = post.querySelector(".post-body");
    updatedText = result.body;
    postBody.innerText = result.body;
}






//  Currently not in use
function publishPost(event) {
	// event.preventDefault(); // prevents form submission reloading current page

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
    console.log(`toggling like of post ${postId}`);
    fetch(`/posts/like/${postId}`, {
        method: 'PUT'})
        .then(response => response.json())
        .then(status => {
            updateLikeButton(postId, status)
        });
}

function updateLikeButton(postId, status) {
    let post = document.querySelector(`[data-postid="${postId}"]`);
    let likeButton = post.querySelector(".heart");
    if (status.liked === true) {
        likeButton.innerHTML = '<i class="fas fa-heart"></i>';
        return;
    }

    likeButton.innerHTML = '<i class="far fa-heart"></i>';
    return;
}
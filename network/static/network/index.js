document.addEventListener("DOMContentLoaded", function () {
	
	addButtonListeners();
});

function loadPosts(type = "all") {
	fetch(`/posts/${type}`)
		.then((response) => response.json())
		.then((posts) => {
			posts.forEach((post) => {
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

}

function addButtonListeners() {

	// If profile exists
	try {
		let profile = document.getElementById('profile');
		if (profile) {
			// Add Follow button functionality if button exists
			let followButton = document.querySelector("#btn-follow");
			if (followButton)
				followButton.addEventListener("click", (event) => toggleFollow(event));
		}
	} catch (e) {
		console.log(e);
	}


	// If posts exist
	let posts = document.getElementById('posts');
	if (posts) {
		document.querySelectorAll(".post-wrapper").forEach((item) => {
			let postId = item.dataset.postid;
	
			let heart = item.querySelector(".heart");
			heart.onclick = function () {
				toggleLike(postId);
			};
	
			addOptionsToItem(item);
		});
	}
}

function addOptionsToItem(item) {
	let options = item.querySelector(".post-options");
	if (options != null) {
		let editButton = options.querySelector(".post-edit");

		editButton.onclick = function () {
			closeEditPosts(); // Close any open post editors

			postBody = item.querySelector(".post-body");
			postEditSpace = item.querySelector(".post-body-edit");
			postBodyContent = postBody.innerHTML;
			postBody.style.display = "none";

			let editPostForm = createEditPostForm();
			input = editPostForm.querySelector("#edit-input");
			input.value = postBodyContent;
			

			// Hide edit button
			editButton.style.display = "none";

			// add form to body
			postEditSpace.appendChild(editPostForm);
			input.style.height = 'auto';
			input.style.height = input.scrollHeight + 'px';
		};
	}
}

function createEditPostForm() {
	let form = document.createElement("form");
	let formInput = document.createElement("textarea");
	let cancelButton = document.createElement("span");
	let submitButton = document.createElement("span");
	form.appendChild(formInput);
	form.className = "post-form";
	form.id = "edit-post-form";
	formInput.className = "form-control";
	formInput.id = "edit-input";
	cancelButton.className = "btn btn-sm btn-secondary post-form-button";
	cancelButton.innerText = "Cancel";
	submitButton.className = "btn btn-sm btn-primary post-form-button";
	submitButton.innerText = "Submit";
	form.appendChild(cancelButton);
	form.appendChild(submitButton);

	cancelButton.onclick = closeEditPosts;
	submitButton.onclick = submitEditPost;

	return form;
}

function closeEditPosts() {
	// Selecting all to ensure no more than 1 can be open at a time
	document.querySelectorAll("#edit-post-form").forEach((form) => {
		post = form.closest(".post-wrapper");
		postOptions = post.querySelector(".post-edit");
		postBody = post.querySelector(".post-body");

		// Unhide post body and edit button
		postBody.style.display = "block";
		postOptions.style.display = "block";

		form.remove();
	});
}

function submitEditPost() {
	form = document.querySelector("#edit-post-form");
	post = form.closest(".post-wrapper");
	postId = post.dataset.postid;

	fetch(`/posts/edit/${postId}`, {
		method: "PUT",
		body: JSON.stringify({
			body: post.querySelector("#edit-input").value,
		}),
	})
		.then((response) => response.json())
		.then((result) => {
			if ("error" in result) {
				return alert(result.error);
			}

			updatePostFromEdit(post, result);
			closeEditPosts();
		});
}

function updatePostFromEdit(post, result) {
	postBody = post.querySelector(".post-body");
	updatedText = result.body;
	postBody.innerText = result.body;
}

function toggleFollow(event) {
	event.preventDefault();
	if (isAuth != "True") {
		location.href = '/login';
	}

	var username = document.querySelector("#username").innerHTML;
	fetch(`/follow/${username}`, {
		method: "PUT",
	})
		.then((response) => response.json())
		.then((status) => {
			updateFollowButton(status);
			updateFollowCounts(username);
			
		});
}

function updateFollowButton(status) {
	followButton = document.querySelector("#btn-follow");
	if (status.following === true) {
		followButton.classList.add("btn-secondary");
		followButton.classList.remove("btn-primary");
		followButton.innerHTML = "Unfollow";
		return;
	}

	followButton.innerHTML = "Follow";
	followButton.classList.add("btn-primary");
	followButton.classList.remove("btn-secondary");
	return;
}

function toggleLike(postId) {
	if (isAuth != "True") {
		location.href = '/login';
	}

	fetch(`/posts/like/${postId}`, {
		method: "PUT",
	})
		.then((response) => response.json())
		.then((status) => {
			updateLikeButton(postId, status);
			let post = getPostById(postId);
			let like_count = post.querySelector(".like-count");

			let output = "";
			if (status.likes > 0) output = `${status.likes} like`;
			if (status.likes > 1) output += "s";

			like_count.innerText = output;
		});
}

function updateLikeButton(postId, status) {
	let post = getPostById(postId);
	let likeButton = post.querySelector(".heart");
	if (status.liked === true) {
		likeButton.innerHTML = '<i class="fas fa-heart"></i>';
		return;
	}

	likeButton.innerHTML = '<i class="far fa-heart"></i>';
	return;
}

function updateFollowCounts(username) {
	fetch(`/${username}/get-follow-counts`)
		.then((response) => response.json())
		.then((result) => {
			let followingCount = document.querySelector('#following-count');
			let followerCount = document.querySelector('#followers-count');
			
			followingCount.innerText = result.following;

			followerCountText = `${result.followers} Follower`;
			if (result.followers != 1)
				followerCountText += 's';

			followerCount.innerText = followerCountText;

		});
}

function getPostById(postId) {
	return document.querySelector(`[data-postid="${postId}"]`);
}

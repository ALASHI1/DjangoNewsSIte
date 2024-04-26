document.addEventListener("DOMContentLoaded", function () {
  const articleId = "{{ article.id }}"; // Replace with the actual article ID
  const likeCount = document.querySelector(".like-number");

  // Function to fetch and update the like count
  function fetchLikeCount() {
    fetch(`/article/${articleId}`, { method: "GET" })
      .then((response) => response.json())
      .then((data) => {
        likeCount.textContent = data.count;
      })
      .catch((error) => console.error("Error fetching like count:", error));
  }

  // Call fetchLikeCount initially
  fetchLikeCount();

  // Set up interval to periodically fetch and update the like count
  const pollingInterval = 10000; // 5 seconds
  const intervalId = setInterval(fetchLikeCount, pollingInterval);

  // Cleanup function to stop the interval when the component unmounts
  function cleanup() {
    clearInterval(intervalId);
  }

  // Return cleanup function (optional, depending on your needs)
  return cleanup;
});

document.addEventListener("DOMContentLoaded", function () {
  const likeButtons = document.querySelectorAll(".like-btn");

  likeButtons.forEach((button) => {
    button.addEventListener("click", () => handleLike(button));
  });

  async function handleLike(button) {
    const articleId = button.dataset.articleId;
    const likeCount = button.parentElement.querySelector(".like-number");

    try {
      const response = await fetch(`/article/${articleId}`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // Empty body or data if needed
      });
      const data = await response.json();
      console.log(data);
      likeCount.textContent = data.count;
    } catch (error) {
      console.error("Error:", error);
    }
  }
});
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

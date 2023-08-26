document.addEventListener("DOMContentLoaded", () => {
    const userList = document.getElementById("user-list");

    // Loop through localStorage to display registered users
    for (let i = 0; i < localStorage.length; i++) {
        const username = localStorage.key(i);
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${username}</span>
            <button class="delete-button" data-username="${username}">Delete</button>
        `;
        userList.appendChild(listItem);
    }

    // Add event listeners to delete buttons
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const username = button.getAttribute("data-username");
            if (username) {
                if (confirm(`Are you sure you want to delete user ${username}?`)) {
                    localStorage.removeItem(username);
                    location.reload();
                }
            }
        });
    });
});

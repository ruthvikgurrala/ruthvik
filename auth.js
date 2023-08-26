// Registration and login functionality

const loginButton = document.getElementById("login-button");
const registerButton = document.getElementById("register-button");
const registerUsername = document.getElementById("register-username");
const registerPassword = document.getElementById("register-password");

if (registerButton) {
    registerButton.addEventListener("click", () => {
        const username = registerUsername.value;
        const password = registerPassword.value;

        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }

        if (localStorage.getItem(username)) {
            alert("Username already exists. Please choose a different username.");
        } else {
            localStorage.setItem(username, password);
            alert("Registration successful!");
            // Redirect the user to the chatbox or another page
            window.location.href = "index.html";
        }
    });
}

if (loginButton) {
    loginButton.addEventListener("click", () => {
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;

        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }

        if (!localStorage.getItem(username)) {
            alert("Username not found. Please register an account.");
        } else {
            const storedPassword = localStorage.getItem(username);

            if (storedPassword === password) {
                sessionStorage.setItem("currentUsername", username);
                window.location.href = "wp7.html.html";
            } else {
                alert("Incorrect password. Please try again.");
            }
        }
    });
}

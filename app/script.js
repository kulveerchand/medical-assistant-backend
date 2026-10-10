
const API_URL = "http://127.0.0.1:8000";


function showRegister() {
    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("registerSection").classList.remove("hidden");
}


function showLogin() {
    document.getElementById("registerSection").classList.add("hidden");
    document.getElementById("loginSection").classList.remove("hidden");
}

async function registerUser() {
    const username = document.getElementById("registerUsername").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    const message = document.getElementById("registerMessage");

    if (!username || !email || !password) {
        message.innerText = "Please fill all fields.";
        return;
    }

    if (password.length < 6) {
        message.innerText = "Password must be at least 6 characters.";
        return;
    }

    try {
        message.innerText = "Creating your account...";

        const response = await fetch(`${API_URL}/users/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await readResponse(response);

        message.innerText = data.message || "Registration successful!";

        // Clear registration password.
        document.getElementById("registerPassword").value = "";

        // Switch to login after successful registration.
        if (response.ok) {
            setTimeout(() => {
                showLogin();

                const loginEmail = document.getElementById("loginEmail");
                if (loginEmail) {
                    loginEmail.value = email;
                }

                document.getElementById("loginMessage").innerText =
                    "Registration successful. Please log in.";
            }, 1000);
        }

    } catch (error) {
        message.innerText = error.message || "Cannot connect to backend.";
        console.error("Registration error:", error);
    }
}


async function loginUser() {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    const message = document.getElementById("loginMessage");

    if (!email || !password) {
        message.innerText = "Please enter email and password.";
        return;
    }

    try {
        message.innerText = "Logging in...";

        const response = await fetch(`${API_URL}/users/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await readResponse(response);

        if (
            response.ok &&
            data.user_id !== undefined &&
            data.user_id !== null
        ) {
            // Save the logged-in user's information.
            localStorage.setItem("user_id", String(data.user_id));
            localStorage.setItem("username", data.username || "User");
            localStorage.setItem("email", data.email || email);

            message.innerText = "Login successful! Opening dashboard...";

            // Open dashboard.
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 500);

        } else {
            message.innerText =
                data.message || data.detail || "Login failed.";
        }

    } catch (error) {
        message.innerText =
            error.message || "Cannot connect to backend.";

        console.error("Login error:", error);
    }
}


async function readResponse(response) {
    const text = await response.text();

    let data = {};

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = { detail: text };
        }
    }

    if (!response.ok) {
        const detail = data.detail || data.message || "Request failed.";

        throw new Error(
            typeof detail === "string"
                ? detail
                : JSON.stringify(detail)
        );
    }

    return data;
}

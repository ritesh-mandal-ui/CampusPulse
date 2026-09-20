const API_BASE_URL = "http://127.0.0.1:5000";

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
    const loginMessage = document.getElementById("loginMessage");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        loginMessage.textContent = "Logging in...";

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                loginMessage.textContent = data.error || "Login failed.";
                return;
            }

            localStorage.setItem("token", data.token);
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("email", data.email);
            localStorage.setItem("role", data.role);

            loginMessage.textContent = "Login successful.";

            if (data.role === "STUDENT") {
                window.location.href = "student-dashboard.html";
            } else if (
                data.role === "TPO" ||
                data.role === "ADMIN" ||
                data.role === "SUPER_ADMIN"
            ) {
                window.location.href = "admin-dashboard.html";
            } else {
                loginMessage.textContent = "Unknown user role.";
            }
        } catch (error) {
            loginMessage.textContent =
                "Unable to connect to CampusPulse backend.";
        }
    });
}

if (registerForm) {
    const registerMessage = document.getElementById("registerMessage");

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const role = document.getElementById("role").value;

        registerMessage.textContent = "Creating account...";

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    role: role
                })
            });

            const data = await response.json();

            if (!response.ok) {
                registerMessage.textContent =
                    data.error || "Registration failed.";
                return;
            }

            registerMessage.textContent =
                "Registration successful. Redirecting to login...";

            setTimeout(function () {
                window.location.href = "login.html";
            }, 1000);
        } catch (error) {
            registerMessage.textContent =
                "Unable to connect to CampusPulse backend.";
        }
    });
}
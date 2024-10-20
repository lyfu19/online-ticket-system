function changeLanguage(lang) {
    console.log(translations.languageChanged + ': ' + lang);
    document.getElementById("languageModal").style.display = "none";
}

function showError(elementId, message) {
    var errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = "block";
}

function hideError(elementId) {
    var errorElement = document.getElementById(elementId);
    errorElement.style.display = "none";
}

function validateEmail(email) {
    const re =
        /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function updateNavBar(isLoggedIn, email = "") {
    var nav = document.querySelector("nav ul");
    var welcomeMessage = document.getElementById("welcome-message");
    var placeholder = document.querySelector(".nav-placeholder");

    if (isLoggedIn) {
        nav.innerHTML = `
            <li class="nav-placeholder"></li>
            <li><span id="welcome-message">${translations.welcome}, ${email.split("@")[0]}</span></li>
            <li><a href="/">${translations.home}</a></li>
            <li><a href="/my_bookings">${translations.myBookings}</a></li>
            <li><a href="#" id="logout-button">${translations.logout}</a></li>
            <li class="language-dropdown">
                <a href="#" id="language-switch">${translations.language}</a>
                <div class="language-dropdown-content">
                    <a href="${translations.langEN}">English</a>
                    <a href="${translations.langMI}">Te Reo Māori</a>
                    <a href="${translations.langZH}">中文</a>
                </div>
            </li>
        `;
        document.getElementById("logout-button").onclick = logoutHandler;

        welcomeMessage = document.getElementById("welcome-message");
        welcomeMessage.style.display = "flex";
        placeholder.style.width = "0";
    } else {
        nav.innerHTML = `
            <li class="nav-placeholder"></li>
            <li><span id="welcome-message"></span></li>
            <li><a href="/">${translations.home}</a></li>
            <li><a href="#" id="login-button">${translations.login}</a></li>
            <li><a href="#" id="register-button">${translations.register}</a></li>
            <li class="language-dropdown">
                <a href="#" id="language-switch">${translations.language}</a>
                <div class="language-dropdown-content">
                    <a href="${translations.langEN}">English</a>
                    <a href="${translations.langMI}">Te Reo Māori</a>
                    <a href="${translations.langZH}">中文</a>
                </div>
            </li>
        `;
        welcomeMessage = document.getElementById("welcome-message");
        welcomeMessage.style.display = "none";
        placeholder = document.querySelector(".nav-placeholder");
        placeholder.style.width = "150px";
        bindLoginRegisterEvents();
    }
}

function logoutHandler(e) {
    e.preventDefault();
    fetch("/logout", {
        method: "GET",
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                console.log(translations.loggedOut);
                window.location.reload(); // 刷新页面
            }
        })
        .catch((error) => {
            console.error(translations.error + ':', error);
        });
}

function bindLoginRegisterEvents() {
    var loginBtn = document.getElementById("login-button");
    var registerBtn = document.getElementById("register-button");
    if (loginBtn) {
        loginBtn.onclick = function () {
            clearLoginForm();
            document.getElementById("loginModal").style.display = "block";
        };
    }
    if (registerBtn) {
        registerBtn.onclick = function () {
            document.getElementById("registerModal").style.display = "block";
        };
    }
}

function clearLoginForm() {
    document.getElementById("login-email").value = "";
    document.getElementById("login-password").value = "";
    hideError("login-error");
}

document.addEventListener("DOMContentLoaded", function () {
    updateNavBar(isLoggedIn, userEmail);

    bindLoginRegisterEvents();

    document.getElementById("loginForm").onsubmit = function (e) {
        e.preventDefault();
        var email = document.getElementById("login-email").value;
        var password = document.getElementById("login-password").value;

        if (!validateEmail(email)) {
            showError("login-error", translations.validEmailError);
            return;
        }

        hideError("login-error");

        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email, password: password }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    document.getElementById("loginModal").style.display = "none";
                    updateNavBar(true, email);
                    console.log(translations.loggedIn);
                    if (typeof window.onLoginSuccess === "function") {
                        window.onLoginSuccess(); // 调用登录成功的回调函数
                    }
                } else {
                    showError("login-error", data.message);
                }
            })
            .catch((error) => {
                console.error(translations.error + ':', error);
                showError("login-error", translations.genericError);
            });
    };

    document.getElementById("registerForm").onsubmit = function (e) {
        e.preventDefault();
        var email = document.getElementById("register-email").value;
        var password = document.getElementById("register-password").value;
        var confirmPassword = document.getElementById("confirm-password").value;

        if (!validateEmail(email)) {
            showError("register-error", translations.validEmailError);
            return;
        }

        if (password !== confirmPassword) {
            showError("register-error", translations.passwordsMismatch);
            return;
        }

        hideError("register-error");

        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email, password: password }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    document.getElementById("registerModal").style.display = "none";
                    showError("login-error", data.message);
                    document.getElementById("loginModal").style.display = "block";
                } else {
                    showError("register-error", data.message);
                }
            })
            .catch((error) => {
                console.error(translations.error + ':', error);
                showError("register-error", translations.genericError);
            });
    };

    document.getElementById("switch-to-login").onclick = function (e) {
        e.preventDefault();
        document.getElementById("registerModal").style.display = "none";
        document.getElementById("loginModal").style.display = "block";
    };

    document.getElementById("switch-to-register").onclick = function (e) {
        e.preventDefault();
        document.getElementById("loginModal").style.display = "none";
        document.getElementById("registerModal").style.display = "block";
    };

    var modals = document.getElementsByClassName("modal");
    var closeButtons = document.getElementsByClassName("close");

    for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].onclick = function () {
            for (var j = 0; j < modals.length; j++) {
                modals[j].style.display = "none";
            }
        };
    }

    window.onclick = function (event) {
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    };
});
document.addEventListener('DOMContentLoaded', () => {
    // 注册表单
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const settingForm = document.getElementById('settingForm');

    // 注册表单处理逻辑
    if (registerForm) {
        const usernameInput = document.getElementById('username');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const registerMessage = document.getElementById('registerMessage');
        const registerButton = document.getElementById('registerButton');

        registerButton.disabled = true;

        function validateRegisterForm() {
            let isValid = true;
            let errors = [];

            if (usernameInput.value.trim() === '') {
                errors.push('Username cannot be empty.');
                isValid = false;
            }

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailInput.value)) {
                errors.push('Invalid email format.');
                isValid = false;
            }

            if (passwordInput.value !== confirmPasswordInput.value) {
                errors.push('Passwords do not match.');
                isValid = false;
            }

            registerMessage.textContent = errors.join(' ');
            registerMessage.style.color = errors.length > 0 ? 'red' : '';

            registerButton.disabled = !isValid;
        }

        usernameInput.addEventListener('input', validateRegisterForm);
        emailInput.addEventListener('input', validateRegisterForm);
        passwordInput.addEventListener('input', validateRegisterForm);
        confirmPasswordInput.addEventListener('input', validateRegisterForm);

        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const formData = {
                username: usernameInput.value.trim(),
                email: emailInput.value.trim(),
                password: await hashPassword(passwordInput.value),
            };

            try {
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData),
                });

                const result = await response.json();

                if (response.ok) {
                    registerMessage.innerHTML = result.message + ' <a href="/auth/login">Click here to login</a>';
                    registerMessage.style.color = 'green';
                    setTimeout(() => {
                        window.location.href = '/auth/login';
                    }, 2000);
                } else {
                    registerMessage.textContent = result.message || 'Registration failed!';
                    registerMessage.style.color = 'red';
                }
            } catch (error) {
                console.error('Error:', error);
                registerMessage.textContent = 'An unexpected error occurred!';
                registerMessage.style.color = 'red';
            }
        });
    }

    // 登录表单处理逻辑
    if (loginForm) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const loginMessage = document.getElementById('loginMessage');

        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const formData = {
                username: usernameInput.value.trim(),
                password: await hashPassword(passwordInput.value),
            };

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData),
                });

                if (response.ok) {
                    loginMessage.textContent = 'Login successful!';
                    loginMessage.style.color = 'green';
                    window.location.href = '/';
                } else {
                    const result = await response.json();
                    loginMessage.textContent = result.message || 'Login failed!';
                    loginMessage.style.color = 'red';
                }
            } catch (error) {
                console.error('Error:', error);
                loginMessage.textContent = 'An unexpected error occurred!';
                loginMessage.style.color = 'red';
            }
        });
    }

    // 修改信息表单处理逻辑
    if (settingForm) {
        const emailInput = document.getElementById('email');
        const currentPasswordInput = document.getElementById('current_password');
        const newPasswordInput = document.getElementById('new_password');
        const confirmPasswordInput = document.getElementById('confirm_password');
        const settingMessage = document.getElementById('settingMessage');
        const saveButton = document.getElementById('save_settings');

        saveButton.disabled = true;

        function validateSettingsForm() {
            let isValid = true;
            let errors = [];

            if (currentPasswordInput.value.trim() === '') {
                errors.push('Current password is required.');
                isValid = false;
            }

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailInput.value)) {
                errors.push('Invalid email format.');
                isValid = false;
            }

            if (newPasswordInput.value !== confirmPasswordInput.value) {
                errors.push('New passwords do not match.');
                isValid = false;
            }

            settingMessage.textContent = errors.join(' ');
            settingMessage.style.color = errors.length > 0 ? 'red' : '';

            saveButton.disabled = !isValid;
        }

        emailInput.addEventListener('input', validateSettingsForm);
        currentPasswordInput.addEventListener('input', validateSettingsForm);
        newPasswordInput.addEventListener('input', validateSettingsForm);
        confirmPasswordInput.addEventListener('input', validateSettingsForm);

        settingForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const formData = {
                email: emailInput.value.trim(),
                current_password: await hashPassword(currentPasswordInput.value),
                new_password: await hashPassword(newPasswordInput.value),
            };

            try {
                const response = await fetch('/auth/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData),
                });

                const result = await response.json();

                if (response.ok) {
                    settingMessage.textContent = 'Settings updated successfully!';
                    settingMessage.style.color = 'green';
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    settingMessage.textContent = result.message || 'Update failed!';
                    settingMessage.style.color = 'red';
                }
            } catch (error) {
                console.error('Error:', error);
                settingMessage.textContent = 'An unexpected error occurred!';
                settingMessage.style.color = 'red';
            }
        });
    }
});

// 统一的哈希密码函数
async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hash))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}
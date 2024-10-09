document.addEventListener('DOMContentLoaded', () => {
    const modals = {
        register: document.getElementById('registerModal'),
        login: document.getElementById('loginModal'),
        settings: document.getElementById('settingsModal'),
    };

    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const settingForm = document.getElementById('settingForm');

    // 打开模态框
    window.openModal = function(modalId) {
        const modal = modals[modalId];
        if (modal) {
            modal.style.display = 'block';
        }
    };

    // 关闭模态框
    window.closeModal = function(modalId) {
        const modal = modals[modalId];
        if (modal) {
            modal.style.display = 'none';
        }
    };

    // 注册表单逻辑
    if (registerForm) {
        const usernameInput = document.getElementById('registerUsername');
        const emailInput = document.getElementById('registerEmail');
        const passwordInput = document.getElementById('registerPassword');
        const confirmPasswordInput = document.getElementById('registerConfirmPassword');
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

        registerForm.addEventListener('submit', async function(event) {
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
                    registerMessage.textContent = result.message;
                    registerMessage.style.color = 'green';
                    setTimeout(() => {
                        closeModal('register');
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

    // 登录表单逻辑
    if (loginForm) {
        const usernameInput = document.getElementById('loginUsername');
        const passwordInput = document.getElementById('loginPassword');
        const loginMessage = document.getElementById('loginMessage');

        loginForm.addEventListener('submit', async function(event) {
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
                    closeModal('login');
                    window.location.reload();  // 刷新页面
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

    // 设置表单逻辑
    if (settingForm) {
        const emailInput = document.getElementById('settingsEmail');
        const currentPasswordInput = document.getElementById('settingsCurrentPassword');
        const newPasswordInput = document.getElementById('settingsNewPassword');
        const confirmPasswordInput = document.getElementById('settingsConfirmPassword');
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

        settingForm.addEventListener('submit', async function(event) {
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
                        closeModal('settings');  // 关闭设置模态框
                        window.location.reload();  // 刷新页面
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
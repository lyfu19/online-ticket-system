document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const registerMessage = document.getElementById('registerMessage');
    const registerButton = document.getElementById('registerButton');

    // 页面加载时禁用 Register 按钮
    registerButton.disabled = true;

    // 这个函数负责实时验证用户输入
    function validateForm() {
        let isValid = true;
        let errors = [];

        // 验证用户名是否为空
        if (usernameInput.value.trim() === '') {
            errors.push('Username cannot be empty.');
            isValid = false;
        }

        // 验证邮箱格式
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value)) {
            errors.push('Invalid email format.');
            isValid = false;
        }

        // 验证两次密码是否一致
        if (passwordInput.value !== confirmPasswordInput.value) {
            errors.push('Passwords do not match.');
            isValid = false;
        }

        // 更新错误信息
        if (errors.length > 0) {
            registerMessage.textContent = errors.join(' ');
            registerMessage.style.color = 'red';
        } else {
            registerMessage.textContent = '';
        }

        // 根据表单验证结果启用或禁用按钮
        registerButton.disabled = !isValid;
    }

    // 监听输入事件，实时验证用户输入
    usernameInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    confirmPasswordInput.addEventListener('input', validateForm);

    // 提交时再进行最终验证
    registerForm.addEventListener('submit', function (event) {
        let errors = [];

        // 验证用户名是否为空
        if (usernameInput.value.trim() === '') {
            errors.push('Username cannot be empty.');
        }

        // 验证邮箱格式是否正确
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value)) {
            errors.push('Invalid email format.');
        }

        // 验证两次输入的密码是否一致
        if (passwordInput.value !== confirmPasswordInput.value) {
            errors.push('Passwords do not match.');
        }

        // 如果有任何错误，阻止表单提交并显示错误信息
        if (errors.length > 0) {
            event.preventDefault();  // 阻止表单提交
            registerMessage.textContent = errors.join(' ');
            registerMessage.style.color = 'red';
        }
    });
});

async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hash))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}

// 注册表单提交逻辑
const registerForm = document.querySelector('#registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // 阻止表单默认提交

        const username = document.querySelector('#username').value;
        const email = document.querySelector('#email').value;
        const password = document.querySelector('#password').value;

        // 对密码进行哈希处理
        const hashedPassword = await hashPassword(password);

        const formData = {
            username: username,
            email: email,
            password: hashedPassword,  // 发送哈希后的密码
        };

        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            const result = await response.json();

            if (response.ok) {
                document.querySelector('#registerMessage').innerHTML = result.message + ' <a href="/auth/login">Click here to login</a>';
                document.querySelector('#registerMessage').style.color = 'green';  // 成功时显示绿色

                // 注册成功后 2 秒钟跳转到登录页面
                setTimeout(() => {
                    window.location.href = '/auth/login'; // 跳转到登录页面
                }, 2000);
            } else {
                document.querySelector('#registerMessage').textContent = result.message || 'Registration failed!';
                document.querySelector('#registerMessage').style.color = 'red';  // 失败时显示红色
            }
        } catch (error) {
            console.error('Error:', error);
            document.querySelector('#registerMessage').textContent = 'An unexpected error occurred!';
            document.querySelector('#registerMessage').style.color = 'red';  // 错误时显示红色
        }
    });
}

// 登录表单提交逻辑
const loginForm = document.querySelector('#loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // 阻止表单默认提交

        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;

        // 对密码进行哈希处理
        const hashedPassword = await hashPassword(password);

        const formData = {
            username: username,
            password: hashedPassword,
        };

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const result = await response.json();
                document.querySelector('#loginMessage').textContent = result.message;
                document.querySelector('#loginMessage').style.color = 'green';
                // 登录成功，可以在此处进行页面跳转
                window.location.href = '/';
            } else {
                const result = await response.json();
                document.querySelector('#loginMessage').textContent = result.message || 'Login failed!';
                document.querySelector('#loginMessage').style.color = 'red';
            }
        } catch (error) {
            console.error('Error:', error);
            document.querySelector('#loginMessage').textContent = 'An unexpected error occurred!';
            document.querySelector('#loginMessage').style.color = 'red';
        }
    });
}
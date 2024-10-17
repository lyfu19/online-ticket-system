
// 切换下拉菜单显示/隐藏
function toggleDropdown() {
    document.getElementById("settingsDropdown").classList.toggle("show");
}

// 点击模态框外部关闭模态框
window.onclick = function (event) {
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const settingsModal = document.getElementById('settingsModal');
    const languageModal = document.getElementById('languageModal');
    const settingsDropdown = document.getElementById('settingsDropdown');  // 下拉菜单元素
    const gearButton = document.querySelector('.gear-button');  // 设置按钮元素

    if (event.target === loginModal) {
        loginModal.style.display = "none";
    } else if (event.target === registerModal) {
        registerModal.style.display = "none";
    } else if (event.target === settingsModal) {
        settingsModal.style.display = "none";
    } else if (event.target === languageModal) {
        languageModal.style.display = "none";
    }

    // 点击设置按钮外部区域时，关闭下拉菜单
    if (settingsDropdown && !gearButton.contains(event.target)) {
        settingsDropdown.classList.remove('show');
    }
}
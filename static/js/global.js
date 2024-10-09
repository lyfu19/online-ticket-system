

// 点击模态框外部关闭模态框
window.onclick = function(event) {
  const loginModal = document.getElementById('loginModal');
  const registerModal = document.getElementById('registerModal');
  const settingsModal = document.getElementById('settingsModal');

  if (event.target === loginModal) {
      loginModal.style.display = "none";
  } else if (event.target === registerModal) {
      registerModal.style.display = "none";
  } else if (event.target === settingsModal) {
      settingsModal.style.display = "none";
  }
}
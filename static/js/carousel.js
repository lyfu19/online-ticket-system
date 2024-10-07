// 轮播图功能JS
let currentSlide = 1;
const slides = document.querySelector(".slides");
const totalSlides = document.querySelectorAll(".slide").length;

// 初始化 - 显示第一张幻灯片
slides.style.transform = `translateX(-100%)`;

function moveSlide(direction) {
  slides.style.transition = "transform 0.5s ease-in-out";
  currentSlide += direction;

  // 到达最前面，瞬间跳到最后一张副本
  if (currentSlide === 0) {
    slides.style.transform = `translateX(-${currentSlide * 100}%)`;
    setTimeout(() => {
      slides.style.transition = "none";
      currentSlide = totalSlides - 2; // 跳到最后一张
      slides.style.transform = `translateX(-${currentSlide * 100}%)`;
    }, 500);
  }
  // 到达最后面，瞬间跳到第一张副本
  else if (currentSlide === totalSlides - 1) {
    slides.style.transform = `translateX(-${currentSlide * 100}%)`;
    setTimeout(() => {
      slides.style.transition = "none";
      currentSlide = 1; // 跳到第一张
      slides.style.transform = `translateX(-${currentSlide * 100}%)`;
    }, 500);
  } else {
    slides.style.transform = `translateX(-${currentSlide * 100}%)`;
  }
}
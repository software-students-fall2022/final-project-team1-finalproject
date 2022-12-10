const swiper = new Swiper('.swiper-container', {
  // Optional parameters
  init: true,
  effect: "coverflow",
  grabCursor: true,
  loop: true,
  preloadImages: true,
  // pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  },
  centeredSlides: true,
  slidesPerView: 'auto',
  // navigation: {
  //   nextEl: '.swiper-button-next',
  //   prevEl: '.swiper-button-prev',
  // },

});
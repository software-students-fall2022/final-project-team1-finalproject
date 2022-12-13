const swiper = new Swiper('.swiper-container', {
  init: true,
  effect: "cards",
  grabCursor: true,
  // loop: true,
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
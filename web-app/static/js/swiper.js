const swiper = new Swiper('.swiper-container', {
  // Optional parameters
  effect: "cards",
  grabCursor: true,
  loop: true,
  // pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  },
  centeredSlides: true,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

});
(function () {
  var carousel = document.querySelector("[data-carousel]");
  if (!carousel) return;

  var track = carousel.querySelector("[data-carousel-track]");
  var cards = Array.prototype.slice.call(track.children);
  var prevBtn = carousel.querySelector("[data-carousel-prev]");
  var nextBtn = carousel.querySelector("[data-carousel-next]");
  var dots = Array.prototype.slice.call(
    carousel.querySelectorAll("[data-carousel-dot]"),
  );

  var currentIndex = cards.findIndex(function (card) {
    return card.classList.contains("is-active");
  });
  if (currentIndex < 0) currentIndex = 0;

  function update() {
    cards.forEach(function (card, i) {
      card.classList.toggle("is-active", i === currentIndex);
    });
    dots.forEach(function (dot, i) {
      dot.classList.toggle("is-active", i === currentIndex);
    });

    var activeCard = cards[currentIndex];
    var offset =
      activeCard.offsetLeft - (carousel.offsetWidth - activeCard.offsetWidth) / 2;
    track.style.transform = "translateX(" + -offset + "px)";
  }

  function goTo(index) {
    currentIndex = (index + cards.length) % cards.length;
    update();
  }

  if (prevBtn) prevBtn.addEventListener("click", function () { goTo(currentIndex - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { goTo(currentIndex + 1); });
  dots.forEach(function (dot, i) {
    dot.addEventListener("click", function () { goTo(i); });
  });

  window.addEventListener("resize", update);

  update();
})();

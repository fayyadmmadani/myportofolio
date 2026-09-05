(function () {
  var targets = document.querySelectorAll("[data-reveal]");
  if (!targets.length) return;

  // fallback: browser lama tanpa dukungan IntersectionObserver -> tampilkan langsung, jangan sembunyikan selamanya
  if (!("IntersectionObserver" in window)) {
    targets.forEach(function (el) {
      el.classList.add("is-visible");
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target); // cukup animasi sekali, tidak perlu diamati lagi
        }
      });
    },
    { threshold: 0.4 },
  );

  targets.forEach(function (el) {
    observer.observe(el);
  });
})();

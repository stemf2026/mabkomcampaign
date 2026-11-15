/* loader.js — skeleton fade-out + scroll reveal */
(function () {
  "use strict";
  var MIN_MS = 500;
  var start  = performance.now();
  function release() {
    var wait = Math.max(0, MIN_MS - (performance.now() - start));
    setTimeout(function () {
      document.body.classList.remove("is-loading");
      document.body.classList.add("is-loaded");
    }, wait);
  }
  if (document.readyState === "complete") release();
  else window.addEventListener("load", release, { once: true });

  var items = document.querySelectorAll(".reveal");
  if (!items.length) return;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  items.forEach(function (el) { io.observe(el); });
})();

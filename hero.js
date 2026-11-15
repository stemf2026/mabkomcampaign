/* hero.js - cross-fading hero carousel */
(function () {
  "use strict";
  var hero = document.querySelector(".hero");
  if (!hero) return;

  var bgs    = Array.prototype.slice.call(hero.querySelectorAll("[data-hero-bg]"));
  var slides = Array.prototype.slice.call(hero.querySelectorAll("[data-hero-slide]"));
  if (slides.length < 2) return;

  var nextLabel = hero.querySelector("[data-hero-next]");
  var prevBtn   = hero.querySelector("[data-hero-prev]");
  var nextBtn   = hero.querySelector("[data-hero-next-button]");
  var DELAY   = 7000;
  var index   = 0;
  var timer   = null;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function labelFor(el) {
    var h = el.querySelector("h1");
    return h ? h.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function paint(n) {
    index = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle("active", k === index); });
    bgs.forEach(function (b, k) { b.classList.toggle("is-active", k === index); });
    if (nextLabel) nextLabel.textContent = labelFor(slides[(index + 1) % slides.length]);
  }

  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function start() {
    stop();
    if (reduced) return;
    timer = setInterval(function () { paint(index + 1); }, DELAY);
  }
  function go(n) { paint(n); start(); }

  if (prevBtn) prevBtn.addEventListener("click", function () { go(index - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { go(index + 1); });

  hero.addEventListener("mouseenter", stop);
  hero.addEventListener("mouseleave", start);
  hero.addEventListener("focusin",  stop);
  hero.addEventListener("focusout", start);
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) { stop(); } else { start(); }
  });

  paint(0);
  start();
})();
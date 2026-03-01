(function () {
  var slider = document.querySelector('.news-slider');
  if (!slider) return;

  var slides = Array.from(slider.querySelectorAll('.news-slide'));
  var dots = Array.from(slider.querySelectorAll('.news-slider-dot'));
  var prevBtn = slider.querySelector('.news-slider-prev');
  var nextBtn = slider.querySelector('.news-slider-next');
  var counter = slider.querySelector('.news-slider-counter');
  var current = 0;
  var autoTimer = null;

  function goTo(index) {
    slides[current].classList.remove('active');
    if (dots[current]) dots[current].classList.remove('active');
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    if (dots[current]) dots[current].classList.add('active');
    if (counter) counter.textContent = (current + 1) + ' / ' + slides.length;
  }

  function next() { goTo(current + 1); resetAuto(); }
  function prev() { goTo(current - 1); resetAuto(); }

  function resetAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(next, 5000);
  }

  if (prevBtn) prevBtn.addEventListener('click', prev);
  if (nextBtn) nextBtn.addEventListener('click', next);
  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () { goTo(i); resetAuto(); });
  });

  // Touch swipe
  var touchStartX = 0;
  slider.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  slider.addEventListener('touchend', function (e) {
    var diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 50) {
      if (diff < 0) next(); else prev();
    }
  }, { passive: true });

  // Keyboard
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
  });

  if (slides.length > 1) resetAuto();
})();

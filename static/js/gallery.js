// Gallery lightbox — zero dependencies
(function () {
  const lightbox = document.getElementById('lightbox');
  if (!lightbox) return;

  const img = document.getElementById('lightbox-img');
  const caption = document.getElementById('lightbox-caption');
  const counter = document.getElementById('lightbox-counter');
  const items = Array.from(document.querySelectorAll('.gallery-item'));
  let current = 0;

  function open(index) {
    current = index;
    update();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  function update() {
    const item = items[current];
    const photo = item.querySelector('img');
    const cap = item.querySelector('.gallery-caption');
    img.src = photo.src;
    img.alt = photo.alt;
    caption.textContent = cap ? cap.textContent : '';
    counter.textContent = (current + 1) + ' / ' + items.length;
  }

  function next() {
    current = (current + 1) % items.length;
    update();
  }

  function prev() {
    current = (current - 1 + items.length) % items.length;
    update();
  }

  // Open on click
  items.forEach(function (item, i) {
    item.addEventListener('click', function () {
      open(i);
    });
  });

  // Controls
  lightbox.querySelector('.lightbox-close').addEventListener('click', close);
  lightbox.querySelector('.lightbox-prev').addEventListener('click', prev);
  lightbox.querySelector('.lightbox-next').addEventListener('click', next);

  // Close on backdrop click
  lightbox.addEventListener('click', function (e) {
    if (e.target === lightbox) close();
  });

  // Keyboard navigation
  document.addEventListener('keydown', function (e) {
    if (!lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
  });

  // Touch swipe support
  var touchStartX = 0;
  lightbox.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  lightbox.addEventListener('touchend', function (e) {
    var diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 50) {
      if (diff < 0) next();
      else prev();
    }
  }, { passive: true });
})();

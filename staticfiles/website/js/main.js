/* ── NAVBAR TOGGLE (mobile) ── */
function toggleNav() {
  const nav = document.getElementById('mainNav');
  if (nav) nav.classList.toggle('open');
}

/* ── TUTUP DROPDOWN SAAT KLIK DI LUAR ── */
document.addEventListener('click', function (e) {
  if (!e.target.closest('nav')) {
    document.querySelectorAll('.dropdown, .sub-dropdown').forEach(d => {
      d.style.display = '';
    });
  }
});

/* ── TANDAI MENU AKTIF BERDASARKAN URL ── */
document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname;
  document.querySelectorAll('nav a').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  /* ── ANIMASI SCROLL FADE-IN ── */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(
    '.news-card, .dosen-card, .bidang-card, .galeri-item, .stat-item'
  ).forEach(el => {
    el.classList.add('fade-in-up');
    observer.observe(el);
  });
});

/* ── STICKY HEADER SHADOW ── */
window.addEventListener('scroll', function () {
  const header = document.querySelector('.site-header');
  if (header) {
    header.classList.toggle('scrolled', window.scrollY > 10);
  }
});

(function () {
  document.documentElement.className = document.documentElement.className.replace(/\bno-js\b/, 'js');

  window.setTimeout(function () {
    const loader = document.getElementById('site-loader');
    const main = document.querySelector('main');
    if (loader) loader.classList.add('is-hidden');
    if (main) main.setAttribute('aria-busy', 'false');
  }, 3000);
})();

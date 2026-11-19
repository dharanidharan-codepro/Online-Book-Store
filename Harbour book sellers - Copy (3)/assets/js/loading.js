(() => {
  const hide = () => {
    const overlay = document.querySelector(".loading-overlay");
    if (overlay) {
      overlay.classList.add("is-hidden");
      window.setTimeout(() => overlay.remove(), 500);
    }
  };
  if (document.readyState === "complete") window.setTimeout(hide, 120);
  else window.addEventListener("load", () => window.setTimeout(hide, 120), {once:true});
  window.setTimeout(hide, 2400);
})();

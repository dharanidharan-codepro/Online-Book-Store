// Ambient Glowing Stardust & Constellations for Harbour Books
(() => {
  const home = document.querySelector(".home-page");
  if (!home) return;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion) return;

  const heroSection = home.querySelector(".home-readora-hero");
  if (!heroSection) return;

  const canvas = document.createElement("canvas");
  canvas.className = "home-ambient-canvas";
  canvas.style.position = "absolute";
  canvas.style.inset = "0";
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = "0";
  canvas.style.opacity = "0.7";
  heroSection.prepend(canvas);

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  let width = (canvas.width = heroSection.clientWidth);
  let height = (canvas.height = heroSection.clientHeight);

  const resize = () => {
    width = canvas.width = heroSection.clientWidth;
    height = canvas.height = heroSection.clientHeight;
  };
  window.addEventListener("resize", resize);

  const particles = [];
  const particleCount = 28;
  const colors = ["rgba(245, 166, 35, 0.6)", "rgba(56, 189, 248, 0.5)", "rgba(255, 255, 255, 0.4)"];

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 2 + 0.8,
      color: colors[Math.floor(Math.random() * colors.length)],
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      alpha: Math.random() * 0.7 + 0.3,
      alphaSpeed: (Math.random() * 0.01 + 0.005) * (Math.random() > 0.5 ? 1 : -1)
    });
  }

  let animId;
  const render = () => {
    ctx.clearRect(0, 0, width, height);

    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      p.alpha += p.alphaSpeed;

      if (p.alpha <= 0.2 || p.alpha >= 0.8) {
        p.alphaSpeed = -p.alphaSpeed;
      }

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.save();
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle = p.color;
      ctx.shadowBlur = 10;
      ctx.shadowColor = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    animId = requestAnimationFrame(render);
  };

  render();

  window.addEventListener("pagehide", () => {
    cancelAnimationFrame(animId);
  });
})();
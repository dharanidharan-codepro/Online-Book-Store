(() => {
  const host = document.getElementById("readora-effects");
  if (!host) {
    console.error("Readora's animated scene could not start because its container is missing.");
    return;
  }

  const particles = [
    { x: 3, y: 12, type: "sparkle", size: 23, color: "#f5a623", delay: -2 },
    { x: 15, y: 78, type: "book", size: 18, color: "#ffd27a", delay: -6 },
    { x: 22, y: 28, type: "sparkle", size: 17, color: "#4c6d92", delay: -4 },
    { x: 33, y: 88, type: "orb", size: 10, color: "#fff0cc", delay: -8 },
    { x: 39, y: 15, type: "book", size: 23, color: "#ffd27a", delay: -3 },
    { x: 48, y: 71, type: "sparkle", size: 20, color: "#315575", delay: -7 },
    { x: 55, y: 9, type: "orb", size: 9, color: "#fff0cc", delay: -1 },
    { x: 62, y: 38, type: "book", size: 19, color: "#f5a623", delay: -5 },
    { x: 71, y: 86, type: "sparkle", size: 22, color: "#ffd27a", delay: -9 },
    { x: 78, y: 17, type: "book", size: 17, color: "#7893b0", delay: -2 },
    { x: 87, y: 60, type: "orb", size: 11, color: "#f5a623", delay: -6 },
    { x: 97, y: 28, type: "sparkle", size: 18, color: "#ffd27a", delay: -4 },
    { x: 2, y: 48, type: "orb", size: 8, color: "#fff0cc", delay: -7 },
    { x: 29, y: 56, type: "sparkle", size: 15, color: "#315575", delay: -3 },
    { x: 46, y: 47, type: "book", size: 21, color: "#f5a623", delay: -8 },
    { x: 68, y: 57, type: "orb", size: 7, color: "#ffd27a", delay: -1 },
    { x: 98, y: 91, type: "sparkle", size: 16, color: "#7893b0", delay: -5 },
    { x: 97, y: 76, type: "book", size: 27, color: "#fff0cc", delay: -9 },
    { x: 2, y: 93, type: "book", size: 23, color: "#ffd27a", delay: -2 },
    { x: 98, y: 24, type: "sparkle", size: 13, color: "#f5a623", delay: -6 }
  ];
  if (document.body.classList.contains("readora-page")) {
    const readoraPalette = ["#f5a623", "#ffd27a", "#18304f", "#29496b", "#fff0cc"];
    particles.forEach((particle, index) => {
      particle.color = readoraPalette[index % readoraPalette.length];
    });
  }

  const symbols = ["✦", "✧", "✺", "✦"];
  const setParticleStyle = (element, particle, index) => {
    element.style.setProperty("--particle-x", `${particle.x}%`);
    element.style.setProperty("--particle-y", `${particle.y}%`);
    element.style.setProperty("--particle-size", `${particle.size}px`);
    element.style.setProperty("--particle-color", particle.color);
    element.style.setProperty("--particle-delay", `${particle.delay}s`);
    element.style.setProperty("--particle-duration", `${7 + (index % 5) * 1.4}s`);
  };

  if (window.React && window.ReactDOM?.createRoot) {
    const scene = React.createElement(
      React.Fragment,
      null,
      React.createElement("div", { className: "readora-glow readora-glow-one" }),
      React.createElement("div", { className: "readora-glow readora-glow-two" }),
      ...particles.map((particle, index) =>
        React.createElement(
          "span",
          {
            key: index,
            className: `readora-particle readora-particle-${particle.type}`,
            style: {
              "--particle-x": `${particle.x}%`,
              "--particle-y": `${particle.y}%`,
              "--particle-size": `${particle.size}px`,
              "--particle-color": particle.color,
              "--particle-delay": `${particle.delay}s`,
              "--particle-duration": `${7 + (index % 5) * 1.4}s`
            }
          },
          particle.type === "sparkle" ? symbols[index % symbols.length] : null
        )
      )
    );

    host.classList.add("has-react-scene");
    ReactDOM.createRoot(host).render(scene);
  } else {
    const scene = document.createDocumentFragment();
    ["readora-glow-one", "readora-glow-two"].forEach((name) => {
      const glow = document.createElement("div");
      glow.className = `readora-glow ${name}`;
      scene.append(glow);
    });
    particles.forEach((particle, index) => {
      const element = document.createElement("span");
      element.className = `readora-particle readora-particle-${particle.type}`;
      element.textContent = particle.type === "sparkle" ? symbols[index % symbols.length] : "";
      setParticleStyle(element, particle, index);
      scene.append(element);
    });
    host.classList.add("has-css-scene");
    host.append(scene);
  }

  const form = document.getElementById("assistant-form");
  const input = document.getElementById("assistant-input");
  if (form && input) {
    host.parentElement.querySelectorAll(".prompt-chip").forEach((button) => {
      button.addEventListener("click", () => {
        input.value = button.textContent.replace(/^[^\p{L}\p{N}]+/u, "").trim();
        form.requestSubmit();
      });
    });
  }
})();

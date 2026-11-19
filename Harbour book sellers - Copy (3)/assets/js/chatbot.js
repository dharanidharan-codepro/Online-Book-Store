/* Local-only assistant demo. This file is the integration point for a future AI service. */
(() => {
  const prompts = ["A cosy mystery for the weekend","Books like The Quiet Tide","A thoughtful gift under $20"];
  const responseFor = text => {
    const lower = text.toLowerCase();
    let picks;
    if (lower.includes("mystery") || lower.includes("thriller")) picks = ["small-hours","winter-garden"];
    else if (lower.includes("gift") || lower.includes("under")) picks = ["little-lanterns","paper-moons"];
    else if (lower.includes("adventure") || lower.includes("travel")) picks = ["wild-atlas","far-from-here"];
    else if (lower.includes("cosy") || lower.includes("cozy") || lower.includes("quiet")) picks = ["salt-and-sky","small-hours"];
    else picks = ["quiet-tide","good-ground"];
    const books = picks.map(id => window.HarbourBooks.find(id));
    const intro = `Here's a little reading inspiration for “${text}”. These reader-loved titles might be just the thing:`;
    return {intro,books};
  };
  const addMessage = (container, content, type) => {
    const bubble = document.createElement("div");
    bubble.className = `chat-message ${type}`;
    bubble.innerHTML = content;
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
  };
  const render = () => {
    const container = document.querySelector("#chat-messages");
    if (!container) return;
    container.innerHTML = "";
    addMessage(container,`<span class="mock-tag">Readora · demo reply</span>Hi, book lover! I’m Readora, your reading companion. Tell me what you love, and I’ll suggest a few books. <strong>This is a mock experience</strong> — no AI service is connected yet.`,`bot`);
    const suggestions = document.createElement("div");
    suggestions.className = "suggested-prompts";
    suggestions.innerHTML = prompts.map(prompt => `<button type="button" data-prompt="${prompt}">${prompt}</button>`).join("");
    container.appendChild(suggestions);
    container.scrollTop = container.scrollHeight;
  };
  const send = text => {
    const trimmed = text.trim();
    if (!trimmed) return;
    const container = document.querySelector("#chat-messages");
    if (!container) return;
    const safeText = document.createElement("span");
    safeText.textContent = trimmed;
    addMessage(container,safeText.innerHTML,"user");
    const typing = document.createElement("div");
    typing.className = "typing-indicator";
    typing.textContent = "Readora is thinking…";
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
    window.setTimeout(() => {
      if (!typing.isConnected) return;
      typing.remove();
      const {intro,books} = responseFor(trimmed);
      const content = `<span class="mock-tag">Mock recommendation · not AI generated</span>${intro}${books.map(book => `<div class="recommendation-card"><div class="mini-cover cover-${book.tone}">${book.title.split(" ")[0]}</div><div><strong>${book.title}</strong><span class="book-author">${book.author} · $${book.price.toFixed(2)}</span><a href="book-details.html?id=${book.id}">Explore book →</a></div></div>`).join("")}`;
      addMessage(container,content,"bot");
    },650);
  };
  document.addEventListener("click",event => {
    const prompt = event.target.closest("[data-prompt]");
    if (prompt) {
      const input = document.querySelector("#chat-input");
      if (input) input.value = prompt.dataset.prompt;
      document.querySelector("#chat-form")?.requestSubmit();
    }
    if (event.target.closest("#clear-chat")) render();
  });
  document.addEventListener("submit",event => {
    if (event.target.id !== "chat-form") return;
    event.preventDefault();
    const input = event.target.querySelector("#chat-input");
    send(input.value);
    input.value = "";
    input.focus();
  });
  window.HarbourChat = {render,send};
})();

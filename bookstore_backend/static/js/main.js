
document.addEventListener('DOMContentLoaded', function () {
  const loader = document.getElementById('site-loader');
  const main = document.querySelector('main');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (loader) {
      try {
          const seen = sessionStorage.getItem('loader_seen');
          if (seen === '1') {
              loader.classList.add('is-hidden');
              if (main) main.setAttribute('aria-busy', 'false');
          } else {
              sessionStorage.setItem('loader_seen', '1');
              if (reducedMotion) {
                  loader.classList.add('is-hidden');
                  if (main) main.setAttribute('aria-busy', 'false');
              } else {
                  window.addEventListener('load', function () {
                      loader.classList.add('is-hidden');
                      if (main) main.setAttribute('aria-busy', 'false');
                      document.dispatchEvent(new CustomEvent('site:ready'));
                  }, { once: true });
                  setTimeout(function () {
                      loader.classList.add('is-hidden');
                      if (main) main.setAttribute('aria-busy', 'false');
                      document.dispatchEvent(new CustomEvent('site:ready'));
                  }, 3000);
              }
          }
      } catch (error) {
          if (reducedMotion) {
              loader.classList.add('is-hidden');
              if (main) main.setAttribute('aria-busy', 'false');
          } else {
              window.addEventListener('load', function () {
                  loader.classList.add('is-hidden');
                  if (main) main.setAttribute('aria-busy', 'false');
                  document.dispatchEvent(new CustomEvent('site:ready'));
              }, { once: true });
              setTimeout(function () {
                  loader.classList.add('is-hidden');
                  if (main) main.setAttribute('aria-busy', 'false');
                  document.dispatchEvent(new CustomEvent('site:ready'));
              }, 3000);
          }
      }
  }

  const signInTrigger = document.querySelector('.sign-in-trigger');
  const signInModal = document.getElementById('signInModal');
  document.querySelectorAll('.chip-row input[type="radio"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
          const row = radio.closest('.chip-row');
          if (!row) return;
          row.querySelectorAll('.chip').forEach(function (chip) {
              chip.classList.toggle('active', chip.contains(radio) && radio.checked);
          });
      });
  });
  if (signInTrigger && signInModal) {
      const closeSignInModal = function () {
          signInModal.classList.remove('open');
          signInModal.setAttribute('aria-hidden', 'true');
      };
      signInTrigger.addEventListener('click', function () {
          signInModal.classList.add('open');
          signInModal.setAttribute('aria-hidden', 'false');
      });
      const closeBtn = signInModal.querySelector('.modal-close');
      if (closeBtn) closeBtn.addEventListener('click', closeSignInModal);
      signInModal.addEventListener('click', function (event) {
          if (event.target === signInModal) closeSignInModal();
      });
  }

  function escapeHtml(str) {
      if (!str) return '';
      return String(str)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#39;');
  }

  function formatMarkdown(text) {
      if (!text) return '';
      let escaped = escapeHtml(text);
      // bold **text**
      escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // italic *text*
      escaped = escaped.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');
      // line breaks
      escaped = escaped.replace(/\n/g, '<br>');
      return escaped;
  }

  const form = document.getElementById('assistant-form');
  if (form) {
      const input = document.getElementById('assistant-input');
      
      // Allow Enter key to submit
      if (input) {
          input.addEventListener('keydown', function (e) {
              if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  form.dispatchEvent(new Event('submit', { cancelable: true }));
              }
          });
      }

      // Quick prompt chip click handlers
      document.querySelectorAll('.prompt-chip').forEach(function (chip) {
          chip.addEventListener('click', function () {
              if (!input) return;
              const text = chip.textContent.trim().replace(/^[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\s]+/u, '');
              input.value = text;
              form.dispatchEvent(new Event('submit', { cancelable: true }));
          });
      });

      form.addEventListener('submit', function (event) {
          event.preventDefault();
          if (!input || !input.value.trim()) return;
          const msg = input.value.trim();
          const messages = document.querySelector('.chat-messages');
          const userNode = document.createElement('div');
          userNode.className = 'message user';
          const bubble = document.createElement('div');
          bubble.className = 'bubble';
          bubble.textContent = msg;
          userNode.appendChild(bubble);
          messages.appendChild(userNode);
          input.value = '';
          messages.scrollTop = messages.scrollHeight;

          const typing = document.createElement('div');
          typing.className = 'message assistant typing-indicator';
          const avatar = document.createElement('div');
          avatar.className = 'avatar';
          avatar.innerHTML = '<img src="/static/img/readora-ai-logo.jpg" alt="Readora avatar">';
          const bubbleWrap = document.createElement('div');
          bubbleWrap.className = 'bubble';
          bubbleWrap.innerHTML = '<span class="spinner-grow spinner-grow-sm me-1" role="status"></span> Thinking…';
          typing.appendChild(avatar);
          typing.appendChild(bubbleWrap);
          messages.appendChild(typing);
          messages.scrollTop = messages.scrollHeight;

          fetch('/assistant/message/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
              },
              body: JSON.stringify({ message: msg })
          }).then(response => response.json()).then(data => {
              const typingIndicator = messages.querySelector('.typing-indicator');
              if (typingIndicator) typingIndicator.remove();

              const answer = document.createElement('div');
              answer.className = 'message assistant';
              const avatarNode = document.createElement('div');
              avatarNode.className = 'avatar';
              avatarNode.innerHTML = '<img src="/static/img/readora-ai-logo.jpg" alt="Readora avatar">';
              const bubbleNode = document.createElement('div');
              bubbleNode.className = 'bubble';

              let htmlContent = '<div class="reply-text">' + formatMarkdown(data.reply || 'Readora AI is offline.') + '</div>';

              if (data.books && data.books.length > 0) {
                  htmlContent += '<div class="readora-books mt-3 pt-2 border-top" style="border-color: rgba(0,0,0,0.08) !important;">'
                      + '<div class="small fw-bold text-muted mb-2">Recommended books:</div>'
                      + '<div class="d-flex flex-wrap gap-2">';
                  data.books.forEach(b => {
                      htmlContent += '<a href="/books/' + encodeURIComponent(b.slug) + '/" class="btn btn-sm btn-outline-primary text-start d-inline-flex align-items-center gap-1" style="font-size: 0.85rem; border-radius: 999px;">'
                          + '📖 <strong>' + escapeHtml(b.title) + '</strong> <span class="badge bg-secondary ms-1">₹' + escapeHtml(b.price) + '</span></a>';
                  });
                  htmlContent += '</div></div>';
              }

              bubbleNode.innerHTML = htmlContent;
              answer.appendChild(avatarNode);
              answer.appendChild(bubbleNode);
              messages.appendChild(answer);
              messages.scrollTop = messages.scrollHeight;
          }).catch(() => {
              const typingIndicator = messages.querySelector('.typing-indicator');
              if (typingIndicator) typingIndicator.remove();
          });
      });
  }

  // Book detail tabs (Synopsis vs AI Summary)
  const tabButtons = document.querySelectorAll('#book-detail-tabs [data-tab-target]');
  tabButtons.forEach(btn => {
      btn.addEventListener('click', function () {
          tabButtons.forEach(b => b.classList.remove('active'));
          this.classList.add('active');

          const targetSelector = this.getAttribute('data-tab-target');
          const panes = document.querySelectorAll('.tab-content .tab-pane');
          panes.forEach(p => p.classList.add('d-none'));

          const targetPane = document.querySelector(targetSelector);
          if (targetPane) targetPane.classList.remove('d-none');

          if (targetSelector === '#pane-summary') {
              loadBookSummary(false);
          }
      });
  });

  const refreshBtn = document.getElementById('refresh-summary-btn');
  if (refreshBtn) {
      refreshBtn.addEventListener('click', function () {
          loadBookSummary(true);
      });
  }

  function loadBookSummary(forceRefresh) {
      const summaryContainer = document.getElementById('summary-content');
      if (!summaryContainer) return;
      const slug = summaryContainer.dataset.slug || window.location.pathname.split('/').filter(Boolean).at(-1);
      if (!slug) return;
      if (!forceRefresh && summaryContainer.dataset.loaded === 'true') return;

      summaryContainer.innerHTML = '<div class="d-flex align-items-center gap-2 py-3 text-muted"><span class="spinner-border spinner-border-sm" role="status"></span><span>Asking Gemini 3.5 for a fresh summary…</span></div>';

      const url = '/summary/' + encodeURIComponent(slug) + '/' + (forceRefresh ? '?refresh=1' : '');
      fetch(url)
          .then(r => r.json())
          .then(data => {
              if (data.summary) {
                  summaryContainer.innerHTML = '<p class="lead mb-2" style="font-size:1.05rem;line-height:1.7;">' + formatMarkdown(data.summary) + '</p>' + (data.cached ? '<span class="badge bg-secondary-subtle text-secondary small">Cached summary</span>' : '<span class="badge bg-success-subtle text-success small">Freshly generated with Gemini 3.5 ✦</span>');
                  summaryContainer.dataset.loaded = 'true';
              } else {
                  summaryContainer.innerHTML = '<div class="alert alert-warning py-2 mb-0">' + escapeHtml(data.error || 'No summary available.') + '</div>';
              }
          })
          .catch(err => {
              summaryContainer.innerHTML = '<div class="alert alert-danger py-2 mb-0">Failed to load AI summary. Please check your connection.</div>';
          });
  }
});

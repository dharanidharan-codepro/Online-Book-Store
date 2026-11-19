(() => {
  const base = location.pathname.includes("/pages/") ? "../" : "";
  const page = document.body.dataset.page || "home";
  const $ = selector => document.querySelector(selector);
  const money = amount => `$${amount.toFixed(2)}`;
  const escapeHTML = value => String(value).replace(/[&<>"']/g,char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
  const href = target => `${base}${target === "home" ? "index.html" : `pages/${target}.html`}`;
  const link = (target,label,extra="") => `<a href="${href(target)}" ${extra}>${label}</a>`;

  const header = () => {
    if(!$("#ambient-background")){
      const ambient=document.createElement("div");
      ambient.id="ambient-background";
      ambient.setAttribute("aria-hidden","true");
      document.body.insertBefore(ambient,$("#site-header"));
    }
    const links = [
      ["home","Home"],["books","Books"],["bestsellers","Best Sellers"],["new-arrivals","New Arrivals"],["offers","Offers"],["audiobooks","Audio"]
    ];
    $("#site-header").innerHTML = `<div class="announcement">A little something for your next chapter — <span>free shipping on orders over $45</span></div>
      <header class="site-nav"><div class="container nav-inner">
        <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false">☰</button>
        <a href="${href("home")}" aria-label="Harbour Books home"><img class="brand-logo" src="${base}assets/images/harbour-books-logo.jpg" alt="Harbour Books"></a>
        <nav class="primary-links" aria-label="Main navigation">${links.map(([key,label])=>`<a class="${key===page?"active":""}" href="${href(key)}">${label}</a>`).join("")}</nav>
        <div class="nav-actions"><a class="icon-link" href="${href("readora")}" aria-label="Readora AI">✧</a><a class="icon-link" href="${href("wishlist")}" aria-label="Bookshelf">♡</a><a class="icon-link account-link" href="${href("login")}" aria-label="Sign in">♙</a><a class="icon-link" href="${href("cart")}" aria-label="Shopping bag">♧<span class="cart-count" id="cart-count">0</span></a></div>
      </div></header>`;
    $(".menu-toggle").addEventListener("click",event=>{
      const nav=$(".primary-links"),open=nav.classList.toggle("open");
      event.currentTarget.setAttribute("aria-expanded",String(open));
    });
  };

  const footer = () => {
    $("#site-footer").innerHTML = `<footer class="site-footer"><div class="container"><div class="footer-grid">
      <div><a href="${href("home")}"><img class="footer-logo" src="${base}assets/images/harbour-books-logo.jpg" alt="Harbour Books"></a><p class="footer-about">Stories that take you somewhere. Discover thoughtfully chosen books, helpful recommendations, and a little inspiration for every kind of reader.</p><a href="${href("readora")}" class="btn-outline-custom">Meet Readora AI</a></div>
      <div><h3 class="footer-heading">Explore</h3><ul class="footer-links"><li>${link("books","All books")}</li><li>${link("bestsellers","Best sellers")}</li><li>${link("new-arrivals","New arrivals")}</li><li>${link("offers","Current offers")}</li><li>${link("audiobooks","Audiobooks")}</li></ul></div>
      <div><h3 class="footer-heading">Your account</h3><ul class="footer-links"><li>${link("login","Sign in")}</li><li>${link("register","Create account")}</li><li>${link("wishlist","Your bookshelf")}</li><li>${link("cart","Shopping bag")}</li><li>${link("admin","Store dashboard demo")}</li></ul></div>
      <div><h3 class="footer-heading">A note from us</h3><p class="footer-about">We believe every great journey starts with a page turned.</p><span class="book-rating">★★★★★</span><p class="footer-about">Independent spirit. Harbour heart.</p></div>
    </div><div class="footer-bottom"><span>© 2026 Harbour Books. A frontend-only demo.</span><span>Made for readers, with care.</span></div></div></footer>`;
  };

  const pageBanner = (title,crumb="Home") => `<section class="page-banner"><div class="container"><div class="breadcrumb-text">${link("home","Home")} / ${escapeHTML(crumb)}</div><h1>${escapeHTML(title)}</h1></div></section>`;
  const cover = book => `<div class="book-cover cover-${book.tone}"><small>HARBOUR BOOKS</small><strong>${escapeHTML(book.title)}</strong><em>${escapeHTML(book.author)}</em></div>`;
  const card = book => `<article class="book-card" data-book-card="${book.id}">
    <div class="cover-wrap">${book.tag?`<span class="cover-label">${escapeHTML(book.tag)}</span>`:""}${cover(book)}
      <button class="wish-btn ${window.HarbourCart.wishlist().includes(book.id)?"active":""}" type="button" data-wish="${book.id}" aria-label="Save ${escapeHTML(book.title)} to bookshelf">${window.HarbourCart.wishlist().includes(book.id)?"♥":"♡"}</button>
    </div><div class="book-category">${escapeHTML(book.category)}</div><h3 class="book-title"><a href="${href("book-details")}?id=${encodeURIComponent(book.id)}">${escapeHTML(book.title)}</a></h3>
    <div class="book-author">by ${escapeHTML(book.author)}</div><div class="book-rating">★★★★★ <span style="color:#84909b"> ${book.rating.toFixed(1)}</span></div>
    <div class="book-bottom"><div class="book-price">${money(book.price)}${book.oldPrice?`<span class="old-price">${money(book.oldPrice)}</span>`:""}</div><button class="add-cart" type="button" data-add="${book.id}">Add to bag</button></div></article>`;
  const grid = books => books.length ? `<div class="book-grid">${books.map(card).join("")}</div>` : `<div class="empty-state"><div class="empty-icon">⌕</div><h2>No books found</h2><p class="section-intro mx-auto">Try another search or clear your filters to discover something new.</p></div>`;
  const sectionBooks = (title,kicker,books,target,copy="") => `<section class="section"><div class="container"><div class="section-head"><div><div class="eyebrow">${kicker}</div><h2 class="section-title">${title}</h2>${copy?`<p class="section-intro mb-0 mt-2">${copy}</p>`:""}</div>${link(target,"Explore all →",'class="btn-outline-custom"')}</div>${grid(books)}</div></section>`;
  const categoryTiles = () => `<div class="category-grid">${HarbourBooks.categories.map(item=>`<a class="category-tile" href="${href("books")}?category=${encodeURIComponent(item.name)}"><span class="category-icon">${item.icon}</span><strong>${item.name}</strong><small>${item.count}</small></a>`).join("")}</div>`;
  const newsletter = () => `<section class="newsletter"><div class="container newsletter-inner"><div><div class="eyebrow">A note from the harbour</div><h2>A little reading joy, in your inbox.</h2><p>New releases, reader favourites, and occasional surprises. No spam, ever.</p></div><form id="newsletter-form" class="newsletter-form"><label class="visually-hidden" for="newsletter-email">Email address</label><input id="newsletter-email" type="email" placeholder="Your email address" required><button type="submit">Count me in</button><div class="form-feedback" role="status"></div></form></div></section>`;

  const home = () => {
    const books=HarbourBooks.books;
    return `<section class="hero"><div class="hero-ambient" id="hero-ambient" aria-hidden="true"></div><div class="container hero-inner"><div><div class="eyebrow">A bookshop for every kind of reader</div><h1>Your next favourite is waiting.</h1><p class="hero-copy">A well-chosen story can change the shape of an ordinary day. Find the one that feels like it was waiting for you.</p>
      <form class="search-wrap" id="hero-search"><label class="visually-hidden" for="hero-query">Search books, authors, or genres</label><input id="hero-query" type="search" placeholder="Search books, authors, or genres…" aria-label="Search books"><button type="submit">Find a book&nbsp; →</button></form>
      <div class="mt-3">${link("books","Browse the collection","class=\"btn-outline-custom\"")}</div></div>
      <div class="hero-art" aria-label="Original illustrated book stack"><div class="art-orbit"></div><div class="book-float"><small>AN ADVENTURE</small><b>A Wild Atlas</b><small>JONAH REED</small></div><div class="hero-book"><small>A HARBOUR BOOKS PICK</small><strong>The<br>Quiet<br>Tide</strong><em>MARA ELLISON</em></div></div></div></section>
      <div class="service-strip"><div class="container service-grid"><div class="service"><span class="service-icon">↗</span><div><strong>Free shipping over $45</strong><small>A little treat for your book stack</small></div></div><div class="service"><span class="service-icon">♡</span><div><strong>Chosen with care</strong><small>Thoughtful picks for curious minds</small></div></div><div class="service"><span class="service-icon">✧</span><div><strong>Your reading companion</strong><small>Get inspired with Readora</small></div></div></div></div>
      <section class="section section-soft"><div class="container"><div class="section-head"><div><div class="eyebrow">Find your kind of story</div><h2 class="section-title">Browse by mood</h2></div>${link("books","All categories →","class=\"btn-outline-custom\"")}</div>${categoryTiles()}</div></section>
      ${sectionBooks("Stories to fall into","HAND-PICKED FOR YOU",books.slice(0,4),"books","A few favourites to get your next chapter started.")}
      <section class="section section-soft">${`<div class="container"><div class="section-head"><div><div class="eyebrow">Reader favourites</div><h2 class="section-title">The books everyone's talking about</h2></div>${link("bestsellers","See best sellers →","class=\"btn-outline-custom\"")}</div>${grid(books.filter(book=>book.tag==="Bestseller").slice(0,4))}</div>`}</section>
      ${sectionBooks("Fresh off the press","JUST ARRIVED",books.filter(book=>book.published===2026).slice(0,4),"new-arrivals")}
      <section class="section"><div class="container"><div class="readora-panel"><div><div class="eyebrow">Your personal bookish sidekick</div><h2>Meet Readora, your reading companion.</h2><p>Not sure what to read next? Tell Readora what you love, and get a little inspiration for your next favourite. This preview uses clearly labelled mock recommendations.</p>${link("readora","Ask Readora for a recommendation →","class=\"btn-primary-custom\"")}</div><img class="readora-mark" src="${base}assets/images/readora-ai-logo.jpg" alt="Readora AI — your book assistant"></div></div></section>${newsletter()}`;
  };

  const listing = (kind) => {
    const titles={catalog:["All books","A BOOK FOR EVERY MOOD"],bestsellers:["Best sellers","READER FAVOURITES"],"new-arrivals":["New arrivals","JUST LANDED"],offers:["Offers & little treats","GOOD READS, LOVELY PRICES"],audiobooks:["Audiobooks","LET THE STORY FIND YOU"],wishlist:["Your bookshelf","SAVED FOR A LATER CHAPTER"]};
    const [title,kicker]=titles[kind];
    let source=HarbourBooks.books;
    if(kind==="bestsellers") source=source.filter(book=>book.tag==="Bestseller");
    if(kind==="new-arrivals") source=source.filter(book=>book.published===2026);
    if(kind==="offers") source=source.filter(book=>book.oldPrice);
    if(kind==="wishlist") source=source.filter(book=>HarbourCart.wishlist().includes(book.id));
    if(kind==="audiobooks") source=source.filter(book=>["Adventure","Mystery","Literary Fiction","Fantasy"].includes(book.category)).slice(0,8);
    const showFilters=kind==="catalog";
    return `${pageBanner(title,kicker)}<section class="section"><div class="container">${kind==="audiobooks"?`<div class="readora-panel mb-5"><div><div class="eyebrow">Listen anywhere</div><h2>Stories for the in-between moments.</h2><p>Audio editions are a visual preview in this demo. Choose a title to explore its book details.</p></div><div class="hero-book" style="justify-self:center;transform:rotate(0);width:170px;height:215px"><small>NOW PLAYING</small><strong>Stories<br>in the air</strong><em>HARBOUR AUDIO</em></div></div>`:""}
      ${showFilters?`<div class="catalog-layout"><aside class="filter-panel" id="filter-panel"><h3>Find your story</h3><div class="filter-group"><strong>Category</strong>${["Fiction",...new Set(HarbourBooks.books.map(book=>book.category))].map(category=>`<label><input class="category-filter" type="checkbox" value="${escapeHTML(category)}"> ${escapeHTML(category)}</label>`).join("")}</div><div class="filter-group"><strong>Price</strong><label><input class="price-filter" type="radio" name="price" value="under20"> Under $20</label><label><input class="price-filter" type="radio" name="price" value="over20"> $20 and up</label><label><input class="price-filter" type="radio" name="price" value="all" checked> Any price</label></div><button type="button" class="btn-outline-custom w-100" id="clear-filters">Clear filters</button></aside>`:""}
      <div class="${showFilters?"catalog-content":""}"><div class="catalog-toolbar"><div><div class="catalog-search"><input type="search" id="catalog-query" placeholder="Search this collection…" aria-label="Search collection"><button type="button" aria-label="Search">⌕</button></div>${showFilters?`<button type="button" class="btn-outline-custom d-md-none" id="mobile-filters">Filters</button>`:""}</div><select id="sort-books" aria-label="Sort books"><option value="featured">Sort: Featured</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option><option value="rating">Top rated</option><option value="title">Title A–Z</option></select></div><p class="breadcrumb-text" id="result-count"></p><div id="catalog-results">${grid(source)}</div></div>${showFilters?"</div>":""}</div></section>`;
  };

  const details = () => {
    const book=HarbourBooks.find(new URLSearchParams(location.search).get("id"));
    return `${pageBanner("The details","BOOK DETAILS")}<section class="section"><div class="container"><div class="detail-layout"><div class="detail-cover">${cover(book)}</div><div class="detail-copy"><div class="eyebrow">${escapeHTML(book.category)} · ${book.published} edition</div><h1>${escapeHTML(book.title)}</h1><div class="book-author">by ${escapeHTML(book.author)}</div><div class="book-rating mt-2">★★★★★ <span style="color:#84909b">${book.rating.toFixed(1)} · Reader favourite</span></div><p class="description mt-4">${escapeHTML(book.description)}</p><div class="detail-price">${money(book.price)} ${book.oldPrice?`<span class="old-price">${money(book.oldPrice)}</span>`:""}</div><div class="detail-meta"><div><span>Format</span><br>Paperback</div><div><span>Pages</span><br>${book.pages}</div><div><span>ISBN</span><br>${book.isbn}</div><div><span>Availability</span><br>In stock · demo</div></div><div class="mt-4"><label class="visually-hidden" for="detail-quantity">Quantity</label><input class="quantity-input" id="detail-quantity" type="number" min="1" max="20" value="1"><button class="btn-primary-custom" data-add="${book.id}">Add to bag</button> <button class="btn-outline-custom" data-wish="${book.id}">♡ Save for later</button></div><p class="breadcrumb-text mt-3">Free shipping on orders over $45. Demo catalogue — no purchase will be made.</p></div></div><div class="mt-5"><h2 class="section-title">A few kind words</h2><div class="review-row"><span class="stars">★★★★★</span><strong class="ms-2">“One of those books you want to press into a friend's hands.”</strong><p class="book-author mt-2">A reader's note · Demo review</p></div><div class="review-row"><span class="stars">★★★★★</span><strong class="ms-2">“Beautifully observed, and impossible to put down.”</strong><p class="book-author mt-2">A reader's note · Demo review</p></div></div></div></section>${sectionBooks("Keep exploring","YOU MIGHT ALSO LIKE",HarbourBooks.books.filter(item=>item.id!==book.id).slice(0,4),"books")}`;
  };

  const empty = (icon,title,text,button,target) => `<div class="empty-state"><div class="empty-icon">${icon}</div><h2>${title}</h2><p>${text}</p>${link(target,button,'class="btn-primary-custom"')}</div>`;
  const cartPage = () => {
    const items=HarbourCart.cart().map(item=>({...item,book:HarbourBooks.find(item.id)}));
    if(!items.length)return `${pageBanner("Your shopping bag","YOUR BAG")}<section class="section"><div class="container">${empty("♧","Your bag is having a quiet moment.","There are no books in your bag just yet. Find something you'll love.","Browse the books","books")}</div></section>`;
    const subtotal=items.reduce((total,item)=>total+item.book.price*item.quantity,0);
    const shipping=subtotal>=45?0:4.95;
    return `${pageBanner("Your shopping bag","YOUR BAG")}<section class="section"><div class="container cart-layout"><div class="admin-table-wrap"><table class="cart-table"><thead><tr><th>Book</th><th>Price</th><th>Quantity</th><th>Total</th><th></th></tr></thead><tbody>${items.map(item=>`<tr><td><div class="cart-book"><div class="mini-cover cover-${item.book.tone}">${escapeHTML(item.book.title.split(" ")[0])}</div><div><strong>${escapeHTML(item.book.title)}</strong><div class="book-author">${escapeHTML(item.book.author)}</div></div></div></td><td>${money(item.book.price)}</td><td><input class="cart-quantity" data-quantity="${item.id}" type="number" min="1" max="20" value="${item.quantity}" aria-label="Quantity for ${escapeHTML(item.book.title)}"></td><td>${money(item.book.price*item.quantity)}</td><td><button class="icon-link" type="button" data-remove="${item.id}" aria-label="Remove ${escapeHTML(item.book.title)}">×</button></td></tr>`).join("")}</tbody></table></div><aside class="summary-card"><h3>Bag summary</h3><div class="summary-line"><span>Subtotal</span><span>${money(subtotal)}</span></div><div class="summary-line"><span>Demo shipping</span><span>${shipping?money(shipping):"Free"}</span></div><div class="summary-line summary-total"><span>Estimated total</span><span>${money(subtotal+shipping)}</span></div><p class="breadcrumb-text">Demo only — no payment or order is processed.</p>${link("checkout","Continue to checkout →",'class="btn-primary-custom w-100"')}</aside></div></section>`;
  };

  const checkoutPage = () => {
    const items=HarbourCart.cart().map(item=>({...item,book:HarbourBooks.find(item.id)}));
    if(!items.length)return `${pageBanner("Checkout","YOUR BAG")}<section class="section"><div class="container">${empty("♧","Your bag is empty.","Add a book before heading to checkout.","Browse books","books")}</div></section>`;
    const subtotal=items.reduce((sum,item)=>sum+item.book.price*item.quantity,0),shipping=subtotal>=45?0:4.95;
    return `${pageBanner("A few details","DEMO CHECKOUT")}<section class="section"><div class="container cart-layout"><div class="form-shell" style="max-width:none"><h1>Delivery details</h1><p>This form is a local demo. Your information will not be stored or sent.</p><form id="checkout-form"><div class="row g-3"><div class="col-sm-6"><label class="form-label" for="checkout-first">First name</label><input class="form-control" id="checkout-first" autocomplete="given-name" required></div><div class="col-sm-6"><label class="form-label" for="checkout-last">Last name</label><input class="form-control" id="checkout-last" autocomplete="family-name" required></div><div class="col-12"><label class="form-label" for="checkout-email">Email address</label><input class="form-control" id="checkout-email" type="email" autocomplete="email" required></div><div class="col-12"><label class="form-label" for="checkout-address">Street address</label><input class="form-control" id="checkout-address" autocomplete="street-address" required></div><div class="col-sm-6"><label class="form-label" for="checkout-city">City</label><input class="form-control" id="checkout-city" autocomplete="address-level2" required></div><div class="col-sm-6"><label class="form-label" for="checkout-postal">Postal code</label><input class="form-control" id="checkout-postal" autocomplete="postal-code" required></div><div class="col-12"><label class="form-label" for="checkout-note">A delivery note <span class="book-author">(optional)</span></label><textarea class="form-control" id="checkout-note" rows="2"></textarea></div></div><div class="form-feedback text-muted">No payment details requested. This demo does not process orders.</div><button class="btn-primary-custom w-100 mt-3" type="submit">Place demo order · ${money(subtotal+shipping)}</button></form></div><aside class="summary-card"><h3>Your books</h3>${items.map(item=>`<div class="summary-line"><span>${escapeHTML(item.book.title)} × ${item.quantity}</span><span>${money(item.book.price*item.quantity)}</span></div>`).join("")}<div class="summary-line"><span>Shipping</span><span>${shipping?money(shipping):"Free"}</span></div><div class="summary-line summary-total"><span>Total</span><span>${money(subtotal+shipping)}</span></div></aside></div></section>`;
  };

  const accountPage = mode => {
    const register=mode==="register";
    return `${pageBanner(register?"Create your account":"Welcome back",register?"JOIN THE BOOK CLUB":"YOUR READING NOOK")}<section class="section section-soft"><div class="container"><div class="form-shell"><div class="eyebrow">${register?"A new chapter":"Good to see you"}</div><h1>${register?"Join the book club.":"Sign in to your nook."}</h1><p>${register?"Keep your saved books together and discover your next favourite.":"Your bookshelf is right where you left it."} This is a frontend-only demo; there is no real account service.</p><form id="account-form" data-mode="${mode}">${register?`<div class="mb-3"><label class="form-label" for="account-name">Your name</label><input class="form-control" id="account-name" autocomplete="name" required></div>`:""}<div class="mb-3"><label class="form-label" for="account-email">Email address</label><input class="form-control" id="account-email" type="email" autocomplete="email" required></div><div class="mb-3"><label class="form-label" for="account-password">Password</label><input class="form-control" id="account-password" type="password" minlength="8" autocomplete="${register?"new-password":"current-password"}" required><small class="book-author">At least 8 characters. Demo validation only.</small></div>${register?`<div class="mb-3"><label class="form-label" for="account-confirm">Confirm password</label><input class="form-control" id="account-confirm" type="password" minlength="8" required></div>`:""}<button class="btn-primary-custom w-100 mt-2" type="submit">${register?"Create account":"Sign in"}</button><div class="form-feedback" role="status"></div></form><p class="text-center mb-0 mt-3">${register?"Already have an account?": "New to Harbour Books?"} ${link(register?"login":"register",register?"Sign in":"Create one")}</p></div></div></section>`;
  };

  const adminPage = () => `${pageBanner("Store dashboard","FRONTEND PREVIEW")}<section class="section"><div class="container"><div class="d-flex justify-content-between align-items-center gap-3 flex-wrap"><div><div class="eyebrow">A demo view for the shop team</div><p class="section-intro mb-0 mt-2">Sample store data only. No database, admin permissions, or write operations are connected.</p></div><button class="btn-primary-custom" id="add-demo-book">＋ Add demo book</button></div><div class="admin-stats mt-4"><div class="stat-card"><small>Books in catalogue</small><strong>${HarbourBooks.books.length}</strong></div><div class="stat-card"><small>Categories</small><strong>${HarbourBooks.categories.length}</strong></div><div class="stat-card"><small>Demo subscribers</small><strong>128</strong></div><div class="stat-card"><small>Featured titles</small><strong>4</strong></div></div><div class="admin-tabs" role="tablist"><button class="admin-tab active" data-admin-tab="books">Books</button><button class="admin-tab" data-admin-tab="categories">Categories</button><button class="admin-tab" data-admin-tab="subscribers">Subscribers</button><button class="admin-tab" data-admin-tab="featured">Featured</button><button class="admin-tab" data-admin-tab="audio">Audiobooks</button></div><div class="admin-table-wrap" id="admin-table"></div></div></section>`;

  const confirmation = () => `<section class="section section-soft"><div class="container"><div class="form-shell text-center"><div class="empty-icon">✓</div><div class="eyebrow">Your demo checkout is complete</div><h1>Thanks for stopping by.</h1><p>This is only a confirmation preview. No real order was placed and no payment was taken.</p><div class="detail-meta text-start my-4"><div><span>Demo reference</span><br>HB-${Math.random().toString(36).slice(2,8).toUpperCase()}</div><div><span>Status</span><br>Preview only</div></div>${link("books","Keep exploring","class=\"btn-primary-custom\"")}</div></div></section>`;

  const render = () => {
    header();
    footer();
    const renderers={home,catalog:()=>listing("catalog"),bestsellers:()=>listing("bestsellers"),"new-arrivals":()=>listing("new-arrivals"),offers:()=>listing("offers"),audiobooks:()=>listing("audiobooks"),wishlist:()=>listing("wishlist"),details,cart:cartPage,checkout:checkoutPage,login:()=>accountPage("login"),register:()=>accountPage("register"),readora:()=>`${pageBanner("A reading companion with ideas","MEET READORA")}<section class="section section-soft"><div class="container"><div class="chat-window"><div class="chat-head"><img src="${base}assets/images/readora-ai-logo.jpg" alt="Readora AI logo"><div><strong>Readora</strong><small>Bookish inspiration · mock mode</small></div><button id="clear-chat" type="button">Clear chat</button></div><div class="chat-messages" id="chat-messages" aria-live="polite"></div><form class="chat-compose" id="chat-form"><label class="visually-hidden" for="chat-input">Message Readora</label><input id="chat-input" type="text" maxlength="300" placeholder="Tell me what you like to read…" autocomplete="off" required><button type="submit">Send →</button></form></div><p class="breadcrumb-text text-center mt-3">Readora replies are clearly labelled mock recommendations. No AI service or API is connected.</p></div></section>`,admin:adminPage,confirmation};
    $("#app").innerHTML=(renderers[page]||home)();
    loadPageAmbient();
    if(["catalog","bestsellers","new-arrivals","offers","audiobooks","wishlist"].includes(page)) setupListing();
    if(page==="cart")setupCart();
    if(page==="admin")setupAdmin();
    if(page==="readora")window.HarbourChat.render();
    if(page==="home")$("#hero-search").addEventListener("submit",event=>{event.preventDefault();location.href=`${href("books")}?q=${encodeURIComponent($("#hero-query").value.trim())}`;});
    updateCartCount();
  };

  const loadExternalScript = src => new Promise((resolve,reject) => {
    const existing=[...document.scripts].find(script=>script.src===new URL(src,location.href).href);
    if(existing){
      if(existing.dataset.loaded==="true"){resolve();return;}
      existing.addEventListener("load",resolve,{once:true});
      existing.addEventListener("error",()=>reject(new Error(`Unable to load ${src}`)),{once:true});
      return;
    }
    const script=document.createElement("script");
    script.src=src;
    script.onload=()=>{script.dataset.loaded="true";resolve();};
    script.onerror=()=>reject(new Error(`Unable to load ${src}`));
    document.head.appendChild(script);
  });

  const loadPageAmbient = async () => {
    try{
      if(!window.React) await loadExternalScript("https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js");
      if(!window.ReactDOM) await loadExternalScript("https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js");
      if(!window.HarbourAmbient) await loadExternalScript(`${base}assets/js/ambient.js`);
      window.HarbourAmbient.mount();
    }catch(error){
      console.error("Page background animation could not be loaded.",error);
    }
  };

  const setupListing = () => {
    const result=$("#catalog-results"),search=$("#catalog-query"),sort=$("#sort-books"),countLabel=$("#result-count");
    const kind=page;
    const initial=HarbourBooks.books.filter(book=>{
      if(kind==="bestsellers")return book.tag==="Bestseller";
      if(kind==="new-arrivals")return book.published===2026;
      if(kind==="offers")return Boolean(book.oldPrice);
      if(kind==="wishlist")return HarbourCart.wishlist().includes(book.id);
      if(kind==="audiobooks")return ["Adventure","Mystery","Literary Fiction","Fantasy"].includes(book.category);
      return true;
    });
    const params=new URLSearchParams(location.search);
    if(params.get("q"))search.value=params.get("q");
    const categoryParam=params.get("category");
    if(categoryParam)document.querySelectorAll(".category-filter").forEach(input=>input.checked=input.value.toLowerCase()===categoryParam.toLowerCase());
    const refresh=()=>{
      const query=(search.value||"").trim().toLowerCase();
      const categories=[...document.querySelectorAll(".category-filter:checked")].map(input=>input.value);
      const price=document.querySelector(".price-filter:checked")?.value||"all";
      let items=initial.filter(book=>{
        const matchesText=`${book.title} ${book.author} ${book.category} ${book.description}`.toLowerCase().includes(query);
        const matchesCategory=!categories.length||categories.includes(book.category)||(categories.includes("Fiction")&&["Literary Fiction","Mystery","Fantasy","Romance"].includes(book.category));
        const matchesPrice=price==="under20"?book.price<20:price==="over20"?book.price>=20:true;
        return matchesText&&matchesCategory&&matchesPrice;
      });
      if(sort.value==="price-low")items.sort((a,b)=>a.price-b.price);
      if(sort.value==="price-high")items.sort((a,b)=>b.price-a.price);
      if(sort.value==="rating")items.sort((a,b)=>b.rating-a.rating);
      if(sort.value==="title")items.sort((a,b)=>a.title.localeCompare(b.title));
      result.innerHTML=grid(items);
      countLabel.textContent=`Showing ${items.length} ${items.length===1?"book":"books"}${query?` for “${escapeHTML(query)}”`:""}`;
    };
    search.addEventListener("input",refresh);
    sort.addEventListener("change",refresh);
    document.querySelectorAll(".category-filter,.price-filter").forEach(input=>input.addEventListener("change",refresh));
    $("#clear-filters")?.addEventListener("click",()=>{search.value="";document.querySelectorAll(".category-filter").forEach(input=>input.checked=false);document.querySelector('[name="price"][value="all"]').checked=true;sort.value="featured";refresh();});
    $("#mobile-filters")?.addEventListener("click",()=>$("#filter-panel").classList.toggle("mobile-open"));
    $("#catalog-query")?.nextElementSibling?.addEventListener("click",refresh);
    refresh();
  };

  const setupCart = () => {
    document.querySelectorAll("[data-quantity]").forEach(input=>input.addEventListener("change",()=>{
      const quantity=Math.max(1,Math.min(20,Number(input.value)||1));
      HarbourCart.setQuantity(input.dataset.quantity,quantity);
      render();
    }));
  };
  const adminData={
    books:()=>`<table class="admin-table"><thead><tr><th>Title</th><th>Author</th><th>Category</th><th>Price</th><th>Label</th><th>Visibility</th></tr></thead><tbody>${HarbourBooks.books.map(book=>`<tr><td>${escapeHTML(book.title)}</td><td>${escapeHTML(book.author)}</td><td>${escapeHTML(book.category)}</td><td>${money(book.price)}</td><td>${escapeHTML(book.tag||"—")}</td><td><span class="status-pill">Published</span></td></tr>`).join("")}</tbody></table>`,
    categories:()=>`<table class="admin-table"><thead><tr><th>Category</th><th>Icon</th><th>Catalogue note</th><th>Status</th></tr></thead><tbody>${HarbourBooks.categories.map(category=>`<tr><td>${category.name}</td><td>${category.icon}</td><td>${category.count}</td><td><span class="status-pill">Active</span></td></tr>`).join("")}</tbody></table>`,
    subscribers:()=>`<div class="empty-state"><div class="empty-icon">✉</div><h2>Subscriber list preview</h2><p>Subscriber records are intentionally not stored by this frontend. The dashboard shows sample totals only.</p></div>`,
    featured:()=>`<table class="admin-table"><thead><tr><th>Section</th><th>Featured titles</th><th>Placement</th><th>Status</th></tr></thead><tbody><tr><td>Staff favourites</td><td>The Quiet Tide, Good Ground</td><td>Homepage</td><td><span class="status-pill">Visible</span></td></tr><tr><td>Fresh arrivals</td><td>A Wild Atlas, The Blue Hour</td><td>Homepage</td><td><span class="status-pill">Visible</span></td></tr></tbody></table>`,
    audio:()=>`<div class="empty-state"><div class="empty-icon">♫</div><h2>Audiobook management preview</h2><p>Audio titles and playback are presentation-only in this frontend demo.</p></div>`
  };
  const setupAdmin=()=>{
    const table=$("#admin-table");
    const show=tab=>{table.innerHTML=adminData[tab]();document.querySelectorAll(".admin-tab").forEach(button=>button.classList.toggle("active",button.dataset.adminTab===tab));};
    show("books");
    document.querySelectorAll(".admin-tab").forEach(button=>button.addEventListener("click",()=>show(button.dataset.adminTab)));
    $("#add-demo-book").addEventListener("click",()=>toast("Book management is a UI preview; no book was added."));
  };

  const updateCartCount=()=>{const count=$("#cart-count");if(count)count.textContent=HarbourCart.count();};
  const toast=(message,type="success")=>{
    let area=$(".toast-area");
    if(!area){area=document.createElement("div");area.className="toast-area";document.body.appendChild(area);}
    const item=document.createElement("div");item.className=`site-toast ${type==="error"?"error":""}`;item.textContent=message;area.appendChild(item);
    window.setTimeout(()=>item.remove(),2800);
  };
  document.addEventListener("click",event=>{
    const addButton=event.target.closest("[data-add]");
    if(addButton){const quantity=$("#detail-quantity")?Math.max(1,Number($("#detail-quantity").value)||1):1;HarbourCart.add(addButton.dataset.add,quantity);}
    const wishButton=event.target.closest("[data-wish]");
    if(wishButton){const saved=HarbourCart.toggleWish(wishButton.dataset.wish);wishButton.classList.toggle("active",saved);wishButton.textContent=saved?"♥":"♡";if(page==="wishlist")render();}
    const removeButton=event.target.closest("[data-remove]");
    if(removeButton){HarbourCart.remove(removeButton.dataset.remove);render();}
  });
  window.HarbourUI={toast,updateCartCount};
  render();
})();

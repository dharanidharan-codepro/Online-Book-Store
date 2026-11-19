(() => {
  const accents = [
    {x:8,y:18,kind:"sparkle",size:19,delay:-2},
    {x:16,y:74,kind:"orb",size:8,delay:-5},
    {x:23,y:34,kind:"book",size:27,delay:-3},
    {x:31,y:86,kind:"sparkle",size:13,delay:-7},
    {x:38,y:13,kind:"orb",size:6,delay:-1},
    {x:47,y:66,kind:"sparkle",size:21,delay:-4},
    {x:54,y:25,kind:"book",size:22,delay:-8},
    {x:63,y:83,kind:"orb",size:10,delay:-2},
    {x:71,y:14,kind:"sparkle",size:16,delay:-6},
    {x:79,y:63,kind:"book",size:25,delay:-5},
    {x:88,y:32,kind:"orb",size:7,delay:-3},
    {x:94,y:78,kind:"sparkle",size:18,delay:-9},
    {x:13,y:48,kind:"sparkle",size:11,delay:-4},
    {x:43,y:44,kind:"orb",size:6,delay:-6},
    {x:68,y:48,kind:"sparkle",size:12,delay:-1},
    {x:91,y:9,kind:"book",size:19,delay:-7},
    {x:4,y:39,kind:"orb",size:8,delay:-3},
    {x:27,y:57,kind:"book",size:18,delay:-6},
    {x:35,y:5,kind:"sparkle",size:15,delay:-2},
    {x:58,y:54,kind:"book",size:23,delay:-4},
    {x:75,y:91,kind:"sparkle",size:14,delay:-8},
    {x:84,y:48,kind:"orb",size:7,delay:-1},
    {x:97,y:56,kind:"book",size:17,delay:-5},
    {x:5,y:91,kind:"sparkle",size:12,delay:-7},
    {x:51,y:95,kind:"orb",size:8,delay:-2}
  ];
  const glyphs = {sparkle:"✦",orb:"",book:"▱"};
  const roots = new Map();
  const themes = {
    home:{accent:"#078c99",bright:"#d1fcf4",glowOne:"rgba(8,183,196,.38)",glowTwo:"rgba(238,169,75,.28)",soft:"#fbf9f4",sparkle:"✦",book:"▱",orb:""},
    catalog:{accent:"#ae7545",bright:"#f5ca87",glowOne:"rgba(233,169,98,.3)",glowTwo:"rgba(186,127,84,.22)",soft:"#fbf6ef",sparkle:"✧",book:"▱",orb:""},
    details:{accent:"#4779aa",bright:"#a5d8fb",glowOne:"rgba(76,147,204,.3)",glowTwo:"rgba(98,118,187,.22)",soft:"#f1f7fc",sparkle:"✦",book:"◇",orb:""},
    bestsellers:{accent:"#c06b32",bright:"#ffd39a",glowOne:"rgba(245,138,65,.3)",glowTwo:"rgba(220,93,78,.22)",soft:"#fff5ed",sparkle:"★",book:"▱",orb:""},
    "new-arrivals":{accent:"#478c72",bright:"#acf2d0",glowOne:"rgba(73,184,144,.3)",glowTwo:"rgba(135,190,117,.22)",soft:"#f1faf4",sparkle:"✳",book:"▱",orb:""},
    offers:{accent:"#c35569",bright:"#ffc2cd",glowOne:"rgba(237,104,137,.3)",glowTwo:"rgba(248,172,87,.23)",soft:"#fff3f5",sparkle:"✿",book:"◇",orb:""},
    audiobooks:{accent:"#7458ae",bright:"#d2beff",glowOne:"rgba(142,106,223,.33)",glowTwo:"rgba(79,152,214,.22)",soft:"#f6f2ff",sparkle:"♫",book:"◖",orb:""},
    wishlist:{accent:"#bd597e",bright:"#ffc3da",glowOne:"rgba(224,102,153,.29)",glowTwo:"rgba(210,124,177,.22)",soft:"#fff3f8",sparkle:"♡",book:"◇",orb:""},
    cart:{accent:"#a77a2f",bright:"#f7d782",glowOne:"rgba(223,176,72,.3)",glowTwo:"rgba(86,165,157,.2)",soft:"#fbf8ed",sparkle:"✧",book:"▱",orb:""},
    checkout:{accent:"#3f9276",bright:"#a8ebcb",glowOne:"rgba(80,194,144,.3)",glowTwo:"rgba(103,168,221,.2)",soft:"#f0faf5",sparkle:"✓",book:"◇",orb:""},
    confirmation:{accent:"#368b66",bright:"#a9eac3",glowOne:"rgba(76,190,119,.3)",glowTwo:"rgba(236,196,89,.22)",soft:"#f0faf2",sparkle:"✦",book:"✓",orb:""},
    login:{accent:"#7461bd",bright:"#c9bdff",glowOne:"rgba(126,104,213,.34)",glowTwo:"rgba(71,137,197,.23)",soft:"#f5f3ff",sparkle:"✧",book:"◇",orb:""},
    register:{accent:"#318a9c",bright:"#a8eef0",glowOne:"rgba(49,182,192,.3)",glowTwo:"rgba(104,137,213,.22)",soft:"#effafb",sparkle:"✦",book:"▱",orb:""},
    readora:{accent:"#7360e8",bright:"#74e9ff",glowOne:"rgba(112,93,235,.37)",glowTwo:"rgba(44,199,232,.27)",soft:"#f2f2ff",sparkle:"✦",book:"◈",orb:""},
    admin:{accent:"#547ba8",bright:"#a9d1fa",glowOne:"rgba(72,127,186,.3)",glowTwo:"rgba(91,153,172,.2)",soft:"#f1f6fb",sparkle:"⌘",book:"▤",orb:""},
    "order-confirmation":{accent:"#3f9276",bright:"#a8ebcb",glowOne:"rgba(80,194,144,.3)",glowTwo:"rgba(103,168,221,.2)",soft:"#f0faf5",sparkle:"✓",book:"✦",orb:""}
  };
  const currentTheme = () => themes[document.body.dataset.page] || themes.home;

  const AmbientScene = ({theme}) => React.createElement(
    React.Fragment,
    null,
    React.createElement("div",{className:"ambient-glow ambient-glow-one"}),
    React.createElement("div",{className:"ambient-glow ambient-glow-two"}),
    ...accents.map((accent,index) => React.createElement(
      "span",
      {
        key:index,
        className:`ambient-particle ambient-${accent.kind}`,
        style:{
          left:`${accent.x}%`,
          top:`${accent.y}%`,
          fontSize:`${accent.size}px`,
          "--float-delay":`${accent.delay}s`,
          "--float-duration":`${8+(index%5)*1.3}s`
        },
        "aria-hidden":"true"
      },
      theme[accent.kind] ?? glyphs[accent.kind]
    ))
  );

  window.HarbourAmbient = {
    mount() {
      if(!window.React || !window.ReactDOM?.createRoot) return;
      const theme=currentTheme();
      document.body.style.setProperty("--ambient-accent",theme.accent);
      document.body.style.setProperty("--ambient-bright",theme.bright);
      document.body.style.setProperty("--ambient-glow-one",theme.glowOne);
      document.body.style.setProperty("--ambient-glow-two",theme.glowTwo);
      document.body.style.setProperty("--ambient-soft",theme.soft);
      ["ambient-background","hero-ambient"].forEach(id=>{
        const host=document.getElementById(id);
        if(host){
          host.style.setProperty("--ambient-accent",theme.accent);
          host.style.setProperty("--ambient-bright",theme.bright);
          host.style.setProperty("--ambient-glow-one",theme.glowOne);
          host.style.setProperty("--ambient-glow-two",theme.glowTwo);
          host.style.setProperty("--ambient-soft",theme.soft);
          if(!roots.has(id)) roots.set(id,ReactDOM.createRoot(host));
          roots.get(id).render(React.createElement(AmbientScene,{theme}));
        }
      });
    }
  };
})();

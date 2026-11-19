/* Mock storefront catalogue. Replace this data source when integrating the backend. */
window.HarbourBooks = (() => {
  const books = [
    {id:"quiet-tide",title:"The Quiet Tide",author:"Mara Ellison",category:"Literary Fiction",price:18.5,oldPrice:23,rating:4.9,tag:"Bestseller",tone:"teal",published:2026,description:"On a windswept island, a daughter returns to the bookshop her mother left behind—and discovers the stories that shaped a family. A luminous novel about belonging, beginnings, and the courage to come home.",isbn:"978-1-83999-104-2",pages:336},
    {id:"wild-atlas",title:"A Wild Atlas",author:"Jonah Reed",category:"Adventure",price:21,oldPrice:null,rating:4.8,tag:"New",tone:"green",published:2026,description:"A field naturalist sets out across the world's disappearing wild places. Part travelogue, part love letter to the natural world, this is an invitation to look closer.",isbn:"978-1-83999-108-0",pages:288},
    {id:"small-hours",title:"The Small Hours",author:"Leila Winters",category:"Mystery",price:16.75,oldPrice:20,rating:4.7,tag:"Bestseller",tone:"violet",published:2025,description:"Every night at 2:13, a light appears in the house across the water. When the lighthouse keeper vanishes, a quiet coastal town learns that old secrets never stay buried.",isbn:"978-1-83999-096-0",pages:304},
    {id:"good-ground",title:"Good Ground",author:"Elias Monroe",category:"Personal Growth",price:19.95,oldPrice:null,rating:4.9,tag:"Staff pick",tone:"gold",published:2026,description:"Small, thoughtful practices for building a life that feels like your own. A warm and refreshingly practical guide to tending your attention, your relationships, and your days.",isbn:"978-1-83999-111-0",pages:224},
    {id:"paper-moons",title:"Paper Moons",author:"Nina Hart",category:"Romance",price:17.25,oldPrice:22,rating:4.6,tag:"20% off",tone:"rose",published:2025,description:"Two rival illustrators share a tiny studio above a late-night bakery. Their collaboration begins with a contract and ends somewhere neither of them planned.",isbn:"978-1-83999-087-8",pages:320},
    {id:"blue-hour",title:"The Blue Hour",author:"Samira Cole",category:"Literary Fiction",price:22,oldPrice:null,rating:4.8,tag:"New",tone:"blue",published:2026,description:"Three generations of women meet each summer at a house by the sea. This tender, sweeping story follows the things families keep—and the things they finally let go.",isbn:"978-1-83999-115-8",pages:368},
    {id:"curious-minds",title:"Curious Minds",author:"Dr. Kit Rowan",category:"Science",price:20.5,oldPrice:null,rating:4.7,tag:"New",tone:"coral",published:2026,description:"Big questions, clear answers. Explore the curious science hiding in everyday life, from the memory of a smell to the strange geometry of a honeycomb.",isbn:"978-1-83999-120-2",pages:256},
    {id:"winter-garden",title:"The Winter Garden",author:"Avery Brooks",category:"Fantasy",price:18,oldPrice:24,rating:4.9,tag:"Bestseller",tone:"green",published:2025,description:"Behind a walled garden, winter never ends. A young gardener with an impossible gift must decide whether to preserve a beautiful illusion or risk everything for spring.",isbn:"978-1-83999-078-6",pages:400},
    {id:"little-lanterns",title:"Little Lanterns",author:"Poppy Lane",category:"Children",price:14.5,oldPrice:null,rating:4.8,tag:"New",tone:"amber",published:2026,description:"A gentle illustrated tale about a small fox who gathers lost lights to guide his forest friends safely home. A bedtime favourite for curious little dreamers.",isbn:"978-1-83999-131-8",pages:40},
    {id:"slow-living",title:"A Slower Sunday",author:"Maeve Foster",category:"Lifestyle",price:19,oldPrice:25,rating:4.5,tag:"20% off",tone:"gold",published:2025,description:"Make room for softer mornings, slower meals, and the rituals that restore you. A beautifully considered guide to finding a little more breathing space in ordinary life.",isbn:"978-1-83999-083-0",pages:192},
    {id:"far-from-here",title:"Far From Here",author:"Theo Jameson",category:"Adventure",price:23.5,oldPrice:null,rating:4.6,tag:"Staff pick",tone:"blue",published:2024,description:"A brother and sister follow a hand-drawn map through the mountains their grandfather once called home. A generous adventure about shared history and new horizons.",isbn:"978-1-83999-068-7",pages:352},
    {id:"salt-and-sky",title:"Salt & Sky",author:"Rhea Bennett",category:"Romance",price:15.95,oldPrice:19.5,rating:4.7,tag:"Bestseller",tone:"coral",published:2025,description:"A summer of unexpected detours brings a city chef and a quiet harbour town together. A bright, feel-good story full of sea air, second chances, and really good food.",isbn:"978-1-83999-073-1",pages:296}
  ];
  const categories = [
    {name:"Fiction",icon:"✦",count:"240+ books"},
    {name:"Mystery",icon:"⌕",count:"85+ books"},
    {name:"Romance",icon:"♡",count:"120+ books"},
    {name:"Adventure",icon:"↗",count:"76+ books"},
    {name:"Personal Growth",icon:"✺",count:"95+ books"},
    {name:"Children",icon:"☼",count:"110+ books"}
  ];
  const find = id => books.find(book => book.id === id) || books[0];
  const byCategory = category => category === "Fiction" ? books.filter(book => ["Literary Fiction","Mystery","Fantasy","Romance"].includes(book.category)) : books.filter(book => book.category === category);
  return {books,categories,find,byCategory};
})();

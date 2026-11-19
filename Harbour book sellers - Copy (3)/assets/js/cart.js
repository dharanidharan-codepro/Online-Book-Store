(() => {
  const CART_KEY = "harbour-books-demo-cart";
  const WISH_KEY = "harbour-books-demo-bookshelf";
  const read = key => {
    try {
      const value = JSON.parse(localStorage.getItem(key) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (error) {
      console.error(`Could not read ${key}`, error);
      return [];
    }
  };
  const write = (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Could not save ${key}`, error);
      window.HarbourUI?.toast("Your browser could not save this demo change.", "error");
    }
  };
  const cart = () => read(CART_KEY);
  const wishlist = () => read(WISH_KEY);
  const count = () => cart().reduce((total, item) => total + item.quantity, 0);
  const add = (id, quantity = 1) => {
    const current = cart();
    const item = current.find(entry => entry.id === id);
    if (item) item.quantity += quantity;
    else current.push({id,quantity});
    write(CART_KEY,current);
    window.HarbourUI?.updateCartCount();
    window.HarbourUI?.toast("Added to your bag.");
  };
  const setQuantity = (id, quantity) => {
    const next = cart().map(item => item.id === id ? {...item,quantity} : item).filter(item => item.quantity > 0);
    write(CART_KEY,next);
  };
  const remove = id => write(CART_KEY,cart().filter(item => item.id !== id));
  const clear = () => write(CART_KEY,[]);
  const toggleWish = id => {
    const current = wishlist();
    const exists = current.includes(id);
    write(WISH_KEY,exists ? current.filter(item => item !== id) : [...current,id]);
    window.HarbourUI?.toast(exists ? "Removed from your bookshelf." : "Saved to your bookshelf.");
    return !exists;
  };
  window.HarbourCart = {cart,wishlist,count,add,setQuantity,remove,clear,toggleWish};
})();

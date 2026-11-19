(() => {
  document.addEventListener("submit",event => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.id === "newsletter-form") {
      event.preventDefault();
      const message = form.querySelector(".form-feedback");
      if (!form.reportValidity()) return;
      message.textContent = "Thanks for joining us! This demo did not save your email address.";
      message.className = "form-feedback text-success";
      form.reset();
    }
    if (form.id === "account-form") {
      event.preventDefault();
      const password=form.querySelector("#account-password");
      const confirmation=form.querySelector("#account-confirm");
      if(confirmation) confirmation.setCustomValidity(password.value===confirmation.value?"":"Passwords do not match.");
      if (!form.reportValidity()) return;
      if(confirmation) confirmation.setCustomValidity("");
      const message = form.querySelector(".form-feedback");
      message.textContent = form.dataset.mode === "register"
        ? "Registration validated. This is a frontend demo; no account was created."
        : "Sign-in form validated. No authentication service is connected.";
      message.className = "form-feedback text-success";
      form.reset();
    }
    if (form.id === "checkout-form") {
      event.preventDefault();
      if (!form.reportValidity()) return;
      window.HarbourCart.clear();
      window.location.href = "order-confirmation.html?demo=1";
    }
  });
})();

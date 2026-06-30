document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll("button, .button-card");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.add("button-clicked");
      setTimeout(() => button.classList.remove("button-clicked"), 180);
    });
  });

  const fileInput = document.querySelector("#image");
  const captureForm = document.querySelector("#capture-form");

  if (fileInput && captureForm) {
    fileInput.addEventListener("change", () => {
      if (fileInput.files && fileInput.files.length > 0) {
        captureForm.requestSubmit();
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", function() {

  const listItems = document.querySelectorAll("li");
  listItems.forEach(item => {
    item.addEventListener("mouseenter", function() {
      this.style.backgroundColor = "#f0f0f0";
    });
    item.addEventListener("mouseleave", function() {
      this.style.backgroundColor = "";
    });
  });


  const helloBtn = document.getElementById("hello-btn");
  const greetingDiv = document.getElementById("greeting");

  if (helloBtn) {
    helloBtn.addEventListener("click", function() {
      greetingDiv.textContent = "Привіт, користувачу!✨";
      greetingDiv.style.color = "#764ba2";
    });
  }

  const emailForm = document.getElementById("email-form");
  const nameInput = document.getElementById("user-name");
  const emailInput = document.getElementById("user-email");
  const messageInput = document.getElementById("user-message");
  const emailError = document.getElementById("email-error");
  const serverResponse = document.getElementById("server-response");

  if (emailForm) {
    emailForm.addEventListener("submit", async function(event) {
      event.preventDefault();

      const nameValue = nameInput.value.trim();
      const emailValue = emailInput.value.trim();
      const messageValue = messageInput.value.trim();

      if (!emailValue.includes("@")) {
        emailError.textContent = "Помилка: введіть коректний email (має бути @).";
        emailInput.style.border = "2px solid red";
        return;
      }

      emailError.textContent = "";
      emailInput.style.border = "1px solid #ccc";
      serverResponse.textContent = "Надсилаємо дані на сервер...";

      try {
        const response = await fetch("/api/submit", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: nameValue,
            email: emailValue,
            message: messageValue
          })
        });

        if (response.ok) {
          const data = await response.json();
          serverResponse.textContent = "Відповідь сервера: " + data.result.message;
          serverResponse.style.color = "green";
        } else {
          serverResponse.textContent = "Помилка сервера. Перевір routes.py.";
          serverResponse.style.color = "red";
        }
      } catch (error) {
        console.error("Помилка:", error);
        serverResponse.textContent = "Не вдалося зв'язатися з сервером. Перевір, чи запущений FastAPI.";
      }
    });
  }
});
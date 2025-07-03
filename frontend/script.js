console.log("script.js підключено");

async function analyzeUnit() {
  console.log("🔁 analyzeUnit викликана");

  const code = document.getElementById("codeInput").value.trim();
  const resultDiv = document.getElementById("result");

  if (!code) {
    resultDiv.textContent = "Будь ласка, введіть код одиниці";
    return;
  }

  resultDiv.textContent = "Обробка…";

  try {
    console.log("Відправляю код:", code);

    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });

    console.log("Отримано відповідь:", response);

    const data = await response.json();
    console.log("JSON результат:", data);

    if (data.result) {
      resultDiv.textContent = data.result;
    } else if (data.error) {
      resultDiv.textContent = `Помилка: ${data.error}`;
    } else {
      resultDiv.textContent = "Невідома помилка";
    }
  } catch (err) {
    console.error("Помилка при запиті:", err);
    resultDiv.textContent = "Щось пішло не так 😔";
  }
}

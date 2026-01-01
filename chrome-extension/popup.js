document.getElementById("askBtn").addEventListener("click", async () => {
  const question = document.getElementById("question").value;

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  const response = await fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, question })
  });

  const data = await response.json();
  document.getElementById("answer").innerText = data.answer;
});

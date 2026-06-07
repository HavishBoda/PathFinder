export async function sendMessage(userId: string, message: string) {
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });
  const data = await response.json();
  return data.response;
}
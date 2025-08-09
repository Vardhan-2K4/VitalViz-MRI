import { io } from "socket.io-client";

// Use your desktop IP here for mobile access
const socket = io("http://10.1.5.50:5000");

socket.on("connect", () => {
  console.log("✅ Connected to WebSocket with ID:", socket.id);
});

export default socket;

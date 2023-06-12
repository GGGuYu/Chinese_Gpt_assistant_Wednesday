// 创建WebSocket对象
const socket = new WebSocket('ws://localhost:8888');

// 监听WebSocket连接打开事件
socket.addEventListener('open', function (event) {
  console.log('WebSocket连接已打开');
});

// 监听WebSocket接收消息事件
socket.addEventListener('message', function (event) {
  console.log('收到消息:', event.data);
});

// 发送消息方法
function sendMessage(message) {
  socket.send(message);
}
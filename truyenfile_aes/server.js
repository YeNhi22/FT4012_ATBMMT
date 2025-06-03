const WebSocket = require('ws');
const http = require('http');
const url = require('url');
const crypto = require('crypto');

// Tạo HTTP server
const server = http.createServer();
const wss = new WebSocket.Server({ server });

// Lưu trữ các phòng và client
const rooms = new Map();

// Tạo ID ngẫu nhiên
function generateId() {
    return crypto.randomBytes(8).toString('hex');
}

wss.on('connection', (ws, req) => {
    const parameters = url.parse(req.url, true).query;
    const roomId = parameters.room || generateId();
    const role = parameters.role || 'unknown';
    const clientId = generateId();

    // Thêm client vào phòng
    if (!rooms.has(roomId)) {
        rooms.set(roomId, new Set());
    }
    const room = rooms.get(roomId);
    room.add(ws);

    // Gửi thông báo tham gia phòng thành công
    ws.send(JSON.stringify({
        type: 'join_success',
        room: roomId,
        clientId: clientId,
        timestamp: Date.now()
    }));

    // Thông báo có thành viên mới cho các client khác trong phòng
    room.forEach(client => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({
                type: 'user_joined',
                room: roomId,
                role: role,
                clientId: clientId,
                timestamp: Date.now()
            }));
        }
    });

    // Xử lý tin nhắn từ client
    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            // Broadcast tin nhắn đến tất cả client trong phòng (trừ chính nó)
            room.forEach(client => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify({
                        ...data,
                        senderId: clientId,
                        timestamp: Date.now()
                    }));
                }
            });
        } catch (error) {
            console.error('Error parsing message:', error);
        }
    });

    // Xử lý khi client ngắt kết nối
    ws.on('close', () => {
        room.delete(ws);
        
        // Thông báo client rời phòng
        room.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({
                    type: 'user_left',
                    room: roomId,
                    clientId: clientId,
                    timestamp: Date.now()
                }));
            }
        });

        // Xóa phòng nếu không còn client
        if (room.size === 0) {
            rooms.delete(roomId);
        }
    });
});

// Khởi động server
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`WebSocket server running on port ${PORT}`);
});
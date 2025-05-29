import asyncio
import websockets
import json
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

class SecureChatServer:
    def __init__(self):
        self.users = {}  # {username: {websocket, encryption_key}}
        self.user_sessions = {}  # {websocket: username}
        self.chat_history = []  # Store encrypted messages
        
    def derive_key(self, password, salt=b'secure_chat_salt'):
        """Tạo khóa AES từ mật khẩu"""
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return key[:32]  # AES-256 cần 32 bytes
    
    def encrypt_message(self, message, key):
        """Mã hóa tin nhắn bằng AES"""
        # Tạo IV ngẫu nhiên
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Padding tin nhắn
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        
        # Mã hóa
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        # Kết hợp IV và dữ liệu mã hóa
        encrypted_message = iv + encrypted
        return base64.b64encode(encrypted_message).decode()
    
    def decrypt_message(self, encrypted_message, key):
        """Giải mã tin nhắn AES"""
        try:
            encrypted_data = base64.b64decode(encrypted_message.encode())
            iv = encrypted_data[:16]
            encrypted = encrypted_data[16:]
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            padded_data = decryptor.update(encrypted) + decryptor.finalize()
            
            # Loại bỏ padding
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            
            return data.decode()
        except Exception as e:
            return f"[Lỗi giải mã: {str(e)}]"
    
    async def register_user(self, websocket, data):
        """Đăng ký người dùng mới"""
        username = data.get('username')
        encryption_key = data.get('encryption_key')
        
        if username in self.users:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Tên người dùng đã tồn tại!'
            }))
            return False
        
        # Tạo khóa mã hóa từ mật khẩu
        derived_key = self.derive_key(encryption_key)
        
        # Lưu thông tin người dùng
        self.users[username] = {
            'websocket': websocket,
            'encryption_key': derived_key
        }
        self.user_sessions[websocket] = username
        
        await websocket.send(json.dumps({
            'type': 'login_success',
            'username': username
        }))
        
        # Gửi danh sách người dùng online
        await self.broadcast_user_list()
        
        # Gửi lịch sử chat đã mã hóa
        await self.send_chat_history(websocket, derived_key)
        
        return True
    
    async def send_chat_history(self, websocket, key):
        """Gửi lịch sử chat cho người dùng mới"""
        for msg in self.chat_history:
            decrypted_msg = self.decrypt_message(msg['encrypted_content'], key)
            await websocket.send(json.dumps({
                'type': 'message',
                'username': msg['username'],
                'message': decrypted_msg,
                'timestamp': msg['timestamp']
            }))
    
    async def broadcast_user_list(self):
        """Gửi danh sách người dùng online"""
        user_list = list(self.users.keys())
        message = json.dumps({
            'type': 'user_list',
            'users': user_list
        })
        
        # Gửi cho tất cả người dùng đang online
        for user_data in self.users.values():
            try:
                await user_data['websocket'].send(message)
            except:
                pass
    
    async def handle_message(self, websocket, data):
        """Xử lý tin nhắn từ người dùng"""
        username = self.user_sessions.get(websocket)
        if not username:
            return
        
        message = data.get('message')
        if not message:
            return
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        user_key = self.users[username]['encryption_key']
        
        # Mã hóa tin nhắn
        encrypted_message = self.encrypt_message(message, user_key)
        
        # Lưu vào lịch sử
        self.chat_history.append({
            'username': username,
            'encrypted_content': encrypted_message,
            'timestamp': timestamp
        })
        
        # Gửi tin nhắn đã giải mã cho tất cả người dùng
        for target_username, user_data in self.users.items():
            try:
                # Giải mã tin nhắn bằng khóa của từng người dùng
                decrypted_msg = self.decrypt_message(encrypted_message, user_data['encryption_key'])
                
                await user_data['websocket'].send(json.dumps({
                    'type': 'message',
                    'username': username,
                    'message': decrypted_msg,
                    'timestamp': timestamp
                }))
            except:
                pass
    
    async def handle_disconnect(self, websocket):
        """Xử lý khi người dùng ngắt kết nối"""
        username = self.user_sessions.get(websocket)
        if username:
            del self.users[username]
            del self.user_sessions[websocket]
            await self.broadcast_user_list()
    
    async def handle_client(self, websocket):
        """Xử lý kết nối từ client"""
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type')
                    
                    if msg_type == 'login':
                        await self.register_user(websocket, data)
                    elif msg_type == 'message':
                        await self.handle_message(websocket, data)
                    
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Dữ liệu không hợp lệ!'
                    }))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.handle_disconnect(websocket)

# Khởi chạy server
async def main():
    server = SecureChatServer()
    print("🔐 Secure Chat Server đang chạy tại ws://localhost:8765")
    print("📱 Mở file HTML trong trình duyệt để sử dụng")
    
    # Sử dụng cú pháp mới cho websockets
    async with websockets.serve(server.handle_client, "localhost", 8765):
        await asyncio.Future()  # Chạy mãi mãi

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server đã dừng!")
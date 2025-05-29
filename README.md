<h2 align="center">XÂY DỰNG ỨNG DỤNG NHẮN TIN AN TOÀN TRÊN WEB SỬ DỤNG THUẬT TOÁN MÃ HÓA AES</h2>

<p>
Dự án được phát triển bằng Python và Flask framework, ứng dụng thuật toán mã hóa AES (Advanced Encryption Standard) để bảo mật nội dung tin nhắn trong giao tiếp trực tuyến.
</p>

<h3>Tính năng chính</h3>

<ul>
  <li><strong>Hệ thống nhắn tin bảo mật:</strong>
    <ul>
      <li>Mã hóa/giải mã tin nhắn theo thời gian thực</li>
      <li>Bảo vệ nội dung chat bằng khóa AES 256-bit</li>
      <li>Xác thực người dùng trước khi giải mã nội dung</li>
    </ul>
  </li>
  <li><strong>Quản lý khóa mã hóa:</strong>
    <ul>
      <li>Tạo và lưu trữ khóa bí mật an toàn</li>
      <li>Cơ chế chia sẻ khóa giữa các người dùng</li>
      <li>Hỗ trợ nhập khóa thủ công khi cần</li>
    </ul>
  </li>
</ul>

<h3>Công nghệ sử dụng</h3>

<ul>
  <li>Ngôn ngữ lập trình: Python 3</li>
  <li>Web framework: Flask</li>
  <li>Giao diện: HTML, CSS</li>
  <li>Thuật toán mã hóa: AES-256-CBC</li>
  <li>Thư viện bảo mật: PyCryptodome</li>
</ul>

<h3>Hướng dẫn triển khai</h3>

<ol>
  <li>Cài đặt thư viện: <code>pip install websockets cryptography</code></li>
  <li>Khởi chạy server: <code>python server.py</code></li>
  <li>Truy cập ứng dụng:: <code>Click đúp vào file HTML</code></li>
  <li>Đăng ký tài khoản và bắt đầu nhắn tin bảo mật</li>
</ol>

<h3>Giao diện ứng dụng</h3>

<p><strong>Trang chủ ứng dụng nhắn tin bảo mật:</strong></p>
<p align="center">
  <img src="https://github.com/YeNhi22/FT4012_ATBMMT/blob/main/Screenshot%202025-05-29%20231333.png" alt="Giao diện chat bảo mật" width="600">
</p>
<p align="center">
  <img src="https://github.com/YeNhi22/FT4012_ATBMMT/blob/main/Screenshot%202025-05-29%20231648.png" alt="Giao diện chat bảo mật" width="600">
</p>

<p><strong>Quy trình hoạt động:</strong></p>
<ol>
  <li>Người dùng A gửi tin nhắn → hệ thống mã hóa bằng AES</li>
  <li>Tin nhắn mã hóa được truyền qua mạng</li>
  <li>Người dùng B nhận tin → hệ thống giải mã bằng khóa chung</li>
  <li>Hiển thị nội dung gốc cho người dùng B</li>
</ol>

<p>Nguyễn Vũ Yến Nhi - Khoa Công nghệ thông tin, Đại học Đại Nam</p>

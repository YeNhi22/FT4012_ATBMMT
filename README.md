<h2 align="center">ỨNG DỤNG NHẮN TIN AN TOÀN SỬ DỤNG THUẬT TOÁN MÃ HÓA AES</h2>

<p>
Dự án được xây dựng bằng Python và WebSocket, cung cấp giải pháp nhắn tin bảo mật end-to-end sử dụng thuật toán AES (Advanced Encryption Standard) với khóa 256-bit.
</p>

<h3>Tính năng chính</h3>

<ul>
  <li><strong>Hệ thống chat bảo mật:</strong>
    <ul>
      <li>Đăng nhập với tên người dùng và khóa mã hóa</li>
      <li>Mã hóa/giải mã tin nhắn theo thời gian thực</li>
      <li>Bảo mật end-to-end với AES-256-CBC</li>
      <li>Hiển thị danh sách người dùng online</li>
    </ul>
  </li>
  <li><strong>Quản lý khóa mã hóa:</strong>
    <ul>
      <li>Tạo khóa AES từ mật khẩu người dùng</li>
      <li>Lưu trữ khóa an toàn phía server</li>
      <li>Mỗi tin nhắn sử dụng IV ngẫu nhiên</li>
    </ul>
  </li>
  <li><strong>Bảo mật nâng cao:</strong>
    <ul>
      <li>PKCS7 padding cho dữ liệu mã hóa</li>
      <li>Lưu trữ lịch sử chat đã mã hóa</li>
      <li>Xử lý lỗi giải mã an toàn</li>
    </ul>
  </li>
</ul>

<h3>Công nghệ sử dụng</h3>

<ul>
  <li>Ngôn ngữ lập trình: Python 3</li>
  <li>Giao thức real-time: WebSocket</li>
  <li>Thư viện mã hóa: cryptography (AES-256-CBC)</li>
  <li>Giao diện: HTML5, CSS3, JavaScript</li>
  <li>Thuật toán bổ sung: PBKDF2-HMAC-SHA256 để dẫn xuất khóa</li>
</ul>

<h3>Hướng dẫn sử dụng</h3>

<ol>
  <li>Cài đặt thư viện: <code>pip install websockets cryptography</code></li>
  <li>Khởi chạy server: <code>python server.py</code></li>
  <li>Mở file index.html trong trình duyệt</li>
  <li>Nhập tên người dùng và khóa bí mật để đăng nhập</li>
  <li>Bắt đầu nhắn tin an toàn với các người dùng khác</li>
</ol>

<h3>Kiến trúc hệ thống</h3>

<p><strong>Quy trình hoạt động:</strong></p>
<ol>
  <li>Client kết nối WebSocket tới server</li>
  <li>Người dùng nhập khóa bí mật → tạo khóa AES bằng PBKDF2</li>
  <li>Tin nhắn được mã hóa bằng AES-256-CBC với IV ngẫu nhiên</li>
  <li>Server lưu trữ tin nhắn đã mã hóa</li>
  <li>Client nhận tin nhắn → giải mã bằng khóa đã biết</li>
</ol>

<p align="center">
  <img src="https://github.com/YeNhi22/FT4012_ATBMMT/blob/main/AES.png?raw=true" alt="Giao diện chat bảo mật" width="600">
</p>

<p>Nguyễn Vũ Yến Nhi - Khoa Công nghệ thông tin, Đại học Đại Nam</p>

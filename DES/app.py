from flask import Flask, render_template, request, send_file, jsonify
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import os
import io

app = Flask(__name__)

def adjust_key(key):
    """Điều chỉnh key để đảm bảo đúng 8 bytes cho DES"""
    key_bytes = key.encode('utf-8')
    
    if len(key_bytes) < 8:
        return key_bytes.ljust(8, b'\0')
    elif len(key_bytes) > 8:
        h = SHA256.new(key_bytes)
        return h.digest()[:8]
    else:
        return key_bytes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    try:
        # Nhận dữ liệu từ form
        mode = request.form.get('mode')
        key = request.form.get('key')
        
        # Kiểm tra file
        if 'file' not in request.files:
            return jsonify({'Lỗi': 'không có tệp nào được chọn'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'Lỗi': 'Không có tệp nào được chọn'}), 400
        
        # Đọc file
        file_data = file.read()
        
        # Xử lý key
        processed_key = adjust_key(key)
        cipher = DES.new(processed_key, DES.MODE_ECB)
        
        # Mã hóa/Giải mã
        if mode == 'encrypt':
            processed_data = cipher.encrypt(pad(file_data, DES.block_size))
            ext = '.enc'
        else:
            processed_data = unpad(cipher.decrypt(file_data), DES.block_size)
            ext = '.dec'
        
        # Tạo file ảo để trả về
        output_filename = os.path.splitext(file.filename)[0] + ext
        return send_file(
            io.BytesIO(processed_data),
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/octet-stream'
        )
        
    except ValueError as e:
        return jsonify({'Lỗi': f'Khóa được định dạng không hợp lệ: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'Lỗi': f'Đã xảy ra lỗi: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
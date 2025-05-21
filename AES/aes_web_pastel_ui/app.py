
from flask import Flask, render_template, request, send_file, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn file 16MB

def process_file(file, key_str, mode='encrypt'):
    key = key_str.encode('utf-8')
    key = pad(key, 16)
    iv = b'1234567890abcdef'
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with tempfile.NamedTemporaryFile(delete=False) as temp_in:
        file.save(temp_in.name)
        with open(temp_in.name, 'rb') as f:
            data = f.read()

        if mode == 'encrypt':
            result = cipher.encrypt(pad(data, AES.block_size))
            out_filename = 'encrypted.aes'
        else:
            try:
                result = unpad(cipher.decrypt(data), AES.block_size)
                out_filename = 'decrypted_output'
            except ValueError:
                return None, "Sai khóa hoặc dữ liệu không hợp lệ."

    return result, out_filename


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    file = request.files['file']
    key = request.form['key']
    action = request.form['action']

    if not file or not key:
        return "Vui lòng chọn file và nhập mã khóa."

    mode = 'encrypt' if action == 'encrypt' else 'decrypt'
    output_path, error = process_file(file, key, mode)

    if error:
        return error

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

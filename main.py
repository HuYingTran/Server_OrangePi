from flask import Flask, Response, render_template, jsonify, request
import threading

from esp32cam import detect_motion, generate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/orangepi')
def orangepi():
    return render_template('orangepi.html')

@app.route('/esp32cam-stream')
def esp32cam_strean():
    t = threading.Thread(target=detect_motion, args=(10,))
    t.daemon = True
    t.start()
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/esp32cam')
def esp32cam():
    return render_template('esp32cam.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "temperature": 22.5,
        "humidity": 60,
        "status": "OK"
    }
    return jsonify(data)  # Trả về dữ liệu dưới dạng JSON

@app.route('/api/status', methods=['POST'])
def post_status():
    # Nhận dữ liệu JSON từ yêu cầu POST
    status_data = request.json

    # Bạn có thể lưu trữ hoặc xử lý dữ liệu status_data ở đây
    print("Received data:", status_data)

    # Trả về phản hồi
    return jsonify({"message": "Status received", "data": status_data}), 201

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port="5000", debug=True,
            threaded=True, use_reloader=False)

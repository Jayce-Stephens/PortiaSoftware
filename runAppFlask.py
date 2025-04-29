from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/start-capture', methods=['POST'])
def start_capture():
    try:
        # Run tester.py script
        result = subprocess.check_output(['python3', '/Volumes/HUNTER/PortiaSoftware/backend/tester.py'], text=True)
        return jsonify({'message': 'Capture started successfully!', 'output': result}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error running tester.py: {e.output}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
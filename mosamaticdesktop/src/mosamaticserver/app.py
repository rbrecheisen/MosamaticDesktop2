from flask import Flask, request, jsonify

from mosamaticdesktop.tasks.pipeline import Pipeline


app = Flask(__name__)


@app.route('/pipeline', methods=['POST'])
def pipeline():

    # Get request payload
    payload = request.get_json()
    input_dir = payload.get('input_dir', None) 
    config_file_path = payload.get('config_file_path', None)

    # Setup pipeline with given config file and input directory
    # and run it
    if input_dir and config_file_path:
        pipeline = Pipeline(config_file_path)
        pipeline.update_input_dir(input_dir)
        pipeline.run()
        return jsonify({'message': 'Pipeline successfully finished'})
    return jsonify({'message': 'No input directory or configuration file path provided'})


def main():
    app.run(debug=False, use_reloader=False, host='localhost', port=5000)


if __name__ == '__main__':
    main()
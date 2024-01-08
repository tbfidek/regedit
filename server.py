from flask import Flask, render_template, request, jsonify, make_response
import regedit_fct as reg
import winreg 
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    """
    Render the index.html template.

    :return: Rendered HTML template.
    """
    return render_template('index.html')

@app.route('/get_subkeys', methods=['POST'])
def get_subkeys():
    """
    Get subkeys for a given registry key.

    :return: JSON response containing subkeys.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('key')
    root_key = getattr(winreg, root)
    subkeys = reg.enum_all_subkeys(root_key, selected_key)
    return jsonify(subkeys)


@app.route('/get_registry_info', methods=['POST'])
def get_reg_info():
    """
    Get registry information for a given key.

    :return: JSON response containing registry information.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('key')
    root_key = getattr(winreg, root)
    registry_info = reg.get_registry_info(root_key, selected_key)
    return jsonify(registry_info)

@app.route('/rename_reg_value', methods=['POST'])
def save_reg_info():
    """
    Rename a registry value.

    :return: JSON response containing registry information after renaming the value.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('selected_key')
    new_name = data.get('new_name')
    old_name = data.get('old_name')
    new_value = data.get('new_value')
    registry_info = reg.rename_registry_value(root, selected_key, old_name, new_name, new_value)
    return jsonify(registry_info)

@app.route('/delete_reg_value', methods=['POST'])
def delete_reg_value():
    """
    Delete a registry value.

    :return: JSON response containing registry information after deleting the value.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('selected_key')
    value_name = data.get('value_name')
    registry_info = reg.delete_registry_value(root, selected_key, value_name)
    return jsonify(registry_info)

@app.route('/delete_reg_key', methods=['POST'])
def delete_reg_key():
    """
    Delete a registry key.

    :return: JSON response containing registry information after deleting the key.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('selected_key')
    registry_info = reg.delete_registry_key(root, selected_key)
    return jsonify(registry_info)

@app.route('/create_reg_key', methods=['POST'])
def create_reg_key():
    """
    Create a registry key.

    :return: JSON response containing registry information after creating the key.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('selected_key')
    name = data.get('name')
    path = selected_key + '\\' + name
    registry_info = reg.create_registry_key(root, path)
    return jsonify(registry_info)

@app.route('/rename_reg_key', methods=['POST'])
def rename_reg_key():
    """
    Rename a registry key.

    :return: JSON response containing registry information after renaming the key.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    old_key = data.get('old_key')
    new_name = data.get('name')
    registry_info = reg.rename_registry_key(root, old_key, new_name)
    return jsonify(registry_info)

@app.route('/create_reg_value', methods=['POST'])
def create_reg_value():
    """
    Create a registry value.

    :return: JSON response containing registry information after creating the value.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    path = data.get('path')
    name = data.get('name')
    type = data.get('type')
    value = data.get('value')
    registry_info = reg.create_registry_value(root, path, name, type, value)
    return jsonify(registry_info)

@app.route('/search_reg_value', methods=['POST'])
def search_reg_value():
    """
    Search for a value in a registry key or its subkeys.

    :return: JSON response containing registry information for the found value.
    :rtype: string
    """
    data = request.get_json()
    root = data.get('root')
    path = data.get('path')
    name = data.get('name')
    registry_info = reg.find_value_in_registry(root, path, name)
    return jsonify(registry_info)

@app.route('/set_url', methods = ['POST'])
def set_url():
    """
    Set a URL as a cookie.

    :return: Response object.
    :rtype: string
    """
    data = request.get_json()
    url = data.get('url')
    response = make_response()
    response.set_cookie('url', url)
    return response

@app.route('/get_url', methods=["GET"])
def get_url():
    """
    Get a URL from cookies.

    :return: JSON response containing the URL.
    :rtype: string
    """
    return jsonify(request.cookies.get('url'))

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port=5000)

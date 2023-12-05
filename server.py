from flask import Flask, render_template, request, jsonify

import winreg 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')    

def enum_subkeys(root_hkey):
    try:
        root_key = getattr(winreg, root_hkey)
        with winreg.OpenKey(root_key, '', 0, winreg.KEY_READ) as reg_key:
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]
            subkeys = [winreg.EnumKey(reg_key, i) for i in range(num_subkeys)]
            return subkeys
    except OSError as e:
        print(f"Error: {e}")
        return []

import winreg

def enum_all_subkeys(root_key, path=''):
    try:
        with winreg.OpenKey(root_key, path, 0, winreg.KEY_READ) as reg_key:
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]
            subkeys = [winreg.EnumKey(reg_key, i) for i in range(num_subkeys)]
            
            if subkeys:
                for subkey in subkeys:
                    full_path = f"{path}\\{subkey}" if path else subkey
                    print(full_path)
                    enum_all_subkeys(root_key, full_path)
    except OSError as e:
        print(f"Error: {e}")

def enum_all_subkeys_test(root_key, path=''):
    try:
        with winreg.OpenKey(root_key, path, 0, winreg.KEY_READ) as reg_key:
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]
            subkeys = [winreg.EnumKey(reg_key, i) for i in range(num_subkeys)]
            return subkeys
    except OSError as e:
        print(f"Error: {e}")

# Example usage:
#root_hives = [winreg.HKEY_CLASSES_ROOT, winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_USERS, winreg.HKEY_CURRENT_CONFIG]
#for root_hive in root_hives:


@app.route('/get_subkeys', methods=['POST'])
def get_subkeys():
    data = request.get_json()
    root = data.get('root')
    selected_key = data.get('key')
    root_key = getattr(winreg, root)
    subkeys = enum_all_subkeys_test(root_key, selected_key)
    return jsonify(subkeys)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=5000)
import winreg

# general testing
key_path = r"SOFTWARE\\CSSO\\CSSO1"
hive = "HKEY_CURRENT_USER"
new_key_name = "CSSO1"


# ✓ create registry key
def create_registry_key(hive, key_path):
    try:
        root_key = getattr(winreg, hive)
        # open a registry key (create if it doesn't exist)
        key = winreg.CreateKey(root_key, key_path)
        print(f"reg key '{key_path}' created")
        # close the key after use
        winreg.CloseKey(key)
    except Exception as e:
        print(f"error creating reg key: {e}")


# ✓ delete registry key
def delete_registry_key(hive, key_path):
    root_key = getattr(winreg, hive)
    try:
        # open the reg key
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        # recursively delete all subkeys and their values
        winreg.DeleteKey(key, "")
        
        # close the key after deleting
        winreg.CloseKey(key)
        
        print(f"Registry key '{key_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error deleting registry key: {e}")


# ? create registry values (string ✓, dword ✓, multi-string ✓, buffer ?)
def create_registry_value(hive, key_path, value_name, value_type, value):
    try:
        root_key = getattr(winreg, hive)
        # open the reg key
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        # create the value
        winreg.SetValueEx(key, value_name, 0, value_type, value)
        
        # close the key after deleting
        winreg.CloseKey(key)
        
        print(f"Registry value '{value_name}' created successfully.")
    except FileNotFoundError:
        print(f"Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error creating registry value: {e}")
#create_registry_value(hive, key_path, "bnn", winreg.REG_DWORD, 0)
#create_registry_value(hive, key_path, "hello", winreg.REG_SZ, "world")
#create_registry_value(hive, key_path, "idk", winreg.REG_MULTI_SZ, ["String1", "String2"])

# ✓ delete a registry key value
def delete_registry_value(hive, key_path, value_name):
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        # delete the specified value from the registry key
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
        
        print(f"reg value '{value_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"reg key '{key_path}' not found.")
    except Exception as e:
        print(f"error deleting reg value: {e}")


# ? rename a registry key - works only for keys with no subkeys
def rename_registry_key1(hive, old_key_path, new_key_name):
    try:
        root_key = getattr(winreg, hive)
        old_key = winreg.OpenKey(root_key, old_key_path, 0, winreg.KEY_READ)
        
        # read the values and subkeys from the old key
        _, num_values, _ = winreg.QueryInfoKey(old_key)

        # open the parent key for the old key
        parent_key_path = "\\".join(old_key_path.split("\\")[:-1])
        parent_key = winreg.OpenKey(root_key, parent_key_path, 0, winreg.KEY_WRITE)

        # create a new key with the desired name
        new_key_path = "\\".join(old_key_path.split("\\")[:-1]) + "\\" + new_key_name
        winreg.CreateKey(parent_key, new_key_name)
        new_key = winreg.OpenKey(parent_key, new_key_name, 0, winreg.KEY_ALL_ACCESS)
        
        # copy values from old key to the new one
        for i in range(num_values):
            value_name, value, value_type = winreg.EnumValue(old_key, i)
            winreg.SetValueEx(new_key, value_name, 0, value_type, value)
        
        # close the keys
        winreg.CloseKey(old_key)
        winreg.CloseKey(new_key)
        winreg.CloseKey(parent_key)
        
        # delete the old key
        winreg.DeleteKey(root_key, old_key_path)
        
        print(f"Registry key '{old_key_path}' renamed to '{new_key_path}' successfully.")
    except FileNotFoundError:
        print(f"Registry key '{old_key_path}' not found.")
    except Exception as e:
        print(f"Error renaming registry key: {e}")


# ✓ rename a registry value
def rename_registry_value(hive, key_path, old_value_name, new_value_name):
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)

        # read the data and type of the old value
        value_data, value_type = winreg.QueryValueEx(key, old_value_name)

        # create a new value with the new name and copy the data
        winreg.SetValueEx(key, new_value_name, 0, value_type, value_data)

        # delete the old value
        winreg.DeleteValue(key, old_value_name)
        winreg.CloseKey(key)
        
        print(f"Registry value '{old_value_name}' renamed to '{new_value_name}' successfully.")
    except FileNotFoundError:
        print(f"Registry key '{key_path}' or value '{old_value_name}' not found.")
    except Exception as e:
        print(f"Error renaming registry value: {e}")
# rename_registry_value("HKEY_CURRENT_USER", key_path, "FileNumber", "filenr")


# ✓ edit a reg value if it is a string
def edit_string_registry_value(hive, key_path, value_name, new_value_data):
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)

        # get the type and current data of the value
        _, value_type = winreg.QueryValueEx(key, value_name)

        # check if it is REG_SZ (string)
        if value_type == winreg.REG_SZ:
            # update the value with the new string data
            winreg.SetValueEx(key, value_name, 0, value_type, new_value_data)
            print(f"String value '{value_name}' in registry updated successfully.")
        else:
            print(f"Value '{value_name}' is not a string type in the registry.")

        winreg.CloseKey(key)
    except FileNotFoundError:
        print(f"Registry key '{key_path}' or value '{value_name}' not found.")
    except Exception as e:
        print(f"Error editing registry value: {e}")
# edit_string_registry_value("HKEY_CURRENT_USER", key_path, "sal", "bine tu?")


# ✓ find a value in a registry key or its subkeys
def find_value_in_registry(hive, key_path, value_name):
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

        # check the values in the current key
        try:
            value_data, value_type = winreg.QueryValueEx(key, value_name)
            print(f"Found value '{value_name}' with data '{value_data}' in key: {key_path}")
        except FileNotFoundError:
            pass  # value not found in the current key
        
        # recursively search in subkeys
        try:
            i = 0
            while True:
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = f"{key_path}\\{subkey_name}"
                find_value_in_registry(hive, subkey_path, value_name)
                i += 1
        except OSError:
            pass 

        winreg.CloseKey(key)
    except FileNotFoundError:
        print(f"Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error searching registry value: {e}")
#find_value_in_registry(hive, key_path, "filenr")
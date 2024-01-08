import winreg

# create key tree
def enum_all_subkeys(root_key, path=''):
    """
    Enumerates all subkeys under a given registry key.

    :param root_key: The root key to start enumerating from.
    :type root_key: string
    :param path: The path of the registry key.
    :type path: string
    :return: A list containing the names of all subkeys.
    :rtype: list 
    """
    try:
        with winreg.OpenKey(root_key, path, 0, winreg.KEY_READ) as reg_key:
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]
            subkeys = [winreg.EnumKey(reg_key, i) for i in range(num_subkeys)]
            return subkeys
    except OSError as e:
        print(f"Error: {e}")


# retrieve registry values for a key
def get_registry_info(root, subkey_path):
    """
    Retrieves registry values for a given key.

    :param root: The root key to start searching from.
    :type root: string
    :param subkey_path: The path of the registry key.
    :type subkey_path: string

    :return: A list containing information about the registry values.
    :rtype: list
    """
    result = []
    try:
        with winreg.OpenKey(root, subkey_path) as key:
            num_vals = winreg.QueryInfoKey(key)[1]
            print(f"Subkey: {subkey_path}")
            print("Name, Value, Type:")
            for i in range(num_vals):
                name, value, type_ = winreg.EnumValue(key, i)
                value_type_str = None
                
                if type_ == winreg.REG_SZ:
                    value_type_str = "REG_SZ"
                elif type_ == winreg.REG_EXPAND_SZ:
                    value_type_str = "REG_EXPAND_SZ"
                elif type_ == winreg.REG_BINARY:
                    value_type_str = "REG_BINARY"
                    result.append([name, value_type_str, value.decode('ISO-8859-1')])
                    continue
                elif type_ == winreg.REG_DWORD:
                    value_type_str = "REG_DWORD"
                    value = hex(value) 

                result.append([name, value_type_str, value])

            
            return result
        
    except FileNotFoundError:
        print("Subkey not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")


# ✓ create registry key
def create_registry_key(hive, key_path):
    """
    Create a new registry key.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key to create.
    :type key_path: string
    """
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
    """
    Delete a registry key and all its subkeys recursively.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key to delete.
    :type key_path: string
    """
    root_key = getattr(winreg, hive)
    old_key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)
    
    subkeys_number, _, _ = winreg.QueryInfoKey(old_key)
    if subkeys_number != 0:
        for i in range(subkeys_number - 1, -1, -1):
            #print(f"I: {i}")
            subkey_path = key_path + '\\' + winreg.EnumKey(old_key, i)
            #print(f"KEY_PATH: {subkey_path}, SUBKEYS_NUMBER: {subkeys_number}")
            subkey = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_ALL_ACCESS)
            subkey_number_next, _, _ = winreg.QueryInfoKey(subkey)
            if subkey_number_next == 0:
                winreg.DeleteKey(root_key, subkey_path)
            else:
                delete_registry_key(hive, subkey_path)

    winreg.DeleteKey(root_key, key_path)
    winreg.CloseKey(old_key)

# ? create registry values (string ✓, dword ✓, multi-string ✓, buffer ?)
def create_registry_value(hive, key_path, value_name, value_type, value):
    """
    Create a new registry value.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key where the value will be created.
    :type key_path: string
    :param value_name: The name of the new value.
    :type value_name: string
    :param value_type: The type of the new value (e.g., "REG_SZ", "REG_DWORD").
    :type value_type: string
    :param value: The data to be stored in the value.
    :type value: string, int, binary
    """
    try:
        root_key = getattr(winreg, hive)
        type = getattr(winreg, value_type)
        # open the reg key
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        # create the value

        if(value_type == "REG_BINARY"):
            value = str.encode(value)
        elif(value_type == "REG_DWORD"):
            value = int(value)

        winreg.SetValueEx(key, value_name, 0, type, value)
        
        # close the key after deleting
        winreg.CloseKey(key)
        
        print(f"Registry value '{value_name}' created successfully.")
    except FileNotFoundError:
        print(f"Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error creating registry value: {e}")


# ✓ delete a registry key value
def delete_registry_value(hive, key_path, value_name):
    """
    Delete a specific value from a registry key.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key.
    :type key_path: string
    :param value_name: The name of the value to delete.
    :type value_name: string
    """
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

def move_values(old_key, new_key):
    """
    Move values from one registry key to another.

    :param old_key: The path of the source registry key.
    :type old_key: string
    :param new_key: The path of the target registry key.
    :type new_key: string
    """
    
    _, subkeys_values_number, _ = winreg.QueryInfoKey(old_key)
    for j in range(subkeys_values_number):
        value_name, value_data, value_type = winreg.EnumValue(old_key, j)
        winreg.SetValueEx(new_key, value_name, 0, value_type, value_data)

def move_subkeys(hive, new_key_path, old_key_path):
    """
    Move subkeys from one registry key to another.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param new_key_path: The path of the target registry key.
    :type new_key_path: string
    :param old_key_path: The path of the source registry key.
    :type old_key_path: string
    """
    try:
        root_key = getattr(winreg, hive)
        old_key = winreg.OpenKey(root_key, old_key_path, 0, winreg.KEY_ALL_ACCESS)
        renamed_key = winreg.CreateKey(root_key, new_key_path)

        move_values(old_key, renamed_key)

        subkeys_number, _, _ = winreg.QueryInfoKey(old_key)
        for i in range(subkeys_number):
            subkey_name = winreg.EnumKey(old_key, i)
            subkey_path = old_key_path + '\\' + subkey_name
            move_subkeys(hive, new_key_path + '\\' + subkey_name, subkey_path)

        winreg.CloseKey(old_key)
        winreg.CloseKey(renamed_key)

    except Exception as e:
        print(f"Error moving subkeys: {e}")

def rename_registry_key(hive, old_key_path, new_key_name):
    """
    Rename a registry key.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param old_key_path: The path of the registry key to rename.
    :type old_key_path: string
    :param new_key_name: The new name for the registry key.
    :type new_key_name: string
    """
    try:
        root_key = getattr(winreg, hive)
        new_key_path = '\\'.join(old_key_path.split('\\')[:-1]) + '\\' + new_key_name

        # check if the new key name already exists
        try:
            winreg.OpenKey(root_key, new_key_path, 0, winreg.KEY_READ)
            raise Exception(f"Registry key '{new_key_name}' already exists.")
        except FileNotFoundError:
            pass
        
        parent_key_path = '\\'.join(old_key_path.split('\\')[:-1])
        parent_key = winreg.OpenKey(root_key, parent_key_path, 0, winreg.KEY_WRITE)
        
        # create a new key with the desired name
        winreg.CreateKey(parent_key, new_key_name)
        move_subkeys(hive, new_key_path, old_key_path)
        delete_registry_key(hive, old_key_path)
        winreg.CloseKey(parent_key)

    except Exception as e:
        print(f"Error renaming registry key: {e}")

    
# ✓ rename a registry value
def rename_registry_value(hive, key_path, old_value_name, new_value_name, new_value):
    """
    Rename a registry value.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key where the value exists.
    :type key_path: string
    :param old_value_name: The current name of the registry value.
    :type old_value_name: string
    :param new_value_name: The new name for the registry value.
    :type new_value_name: string
    :param new_value: The new value data.
    :type new_value: string, int, binary
    """
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_ALL_ACCESS)

        # read the data and type of the old value
        value, value_type = winreg.QueryValueEx(key, old_value_name)

        # create a new value with the new name and copy the data
        if(value_type == 1):
            value = new_value

        winreg.SetValueEx(key, new_value_name, 0, value_type, value)

        # delete the old value
        if old_value_name != new_value_name:
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
    """
    Edit a registry value if it is a string type.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key where the value exists.
    :type key_path: string
    :param value_name: The name of the value to edit.
    :type value_name: string
    :param new_value_data: The new string data for the value.
    :type new_value_data: string
    """
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
    """
    Find a value in a registry key or its subkeys.

    :param hive: The registry hive (e.g., HKEY_CURRENT_USER).
    :type hive: string
    :param key_path: The path of the registry key to start searching.
    :type key_path: string
    :param value_name: The name of the value to find.
    :type value_name: string
    :return: The path of the registry key containing the value, if found.
    :rtype: string
    """
    try:
        root_key = getattr(winreg, hive)
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

        # check the values in the current key
        try:
            value_data, value_type = winreg.QueryValueEx(key, value_name)
            return hive + '\\' + key_path
            #print(f"Found value '{value_name}' with data '{value_data}' in key: {key_path}")
        except FileNotFoundError:
            pass  # value not found in the current key
        
        # recursively search in subkeys
        try:
            i = 0
            while True:
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = f"{key_path}\\{subkey_name}"
                path = find_value_in_registry(hive, subkey_path, value_name)
                if path is not None:
                    return path
                i += 1
        except OSError:
            pass 

        winreg.CloseKey(key)
    except FileNotFoundError:
        print(f"Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error searching registry value: {e}")
#find_value_in_registry(hive, key_path, "filenr")



# rename_registry_key("HKEY_CURRENT_USER", key_path, "salcf10")

# create_registry_value(hive, key_path, "bnnn", winreg.REG_DWORD, 0)
# create_registry_value(hive, key_path, "helllo", winreg.REG_SZ, "world")
# create_registry_value(hive, key_path, "idkk", winreg.REG_MULTI_SZ, ["String1", "String2"])
#create_registry_value(hive, key_path, "idkkkk", winreg.REG_BINARY, b"hello")

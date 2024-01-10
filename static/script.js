const popup = document.getElementById('popup-edit');
const rootList = document.getElementById('rootList');
const registryDiv = document.getElementById('registry');
let location_bar = document.getElementById('location_bar');

window.onload = async function() {
    url = await get_url_cookie();
    if(url != null){
    location_bar.value = url;
    const items = url.split('\\');
    root = document.querySelector('li[data-key="'+ items[0] +'"]');
    selectedKey = root.getAttribute('data-key');
    const subkeys = await fetchSubkeys(selectedKey, '');
    toggleSubkeys(selectedKey, subkeys, root, '');
    displayRegistryInfo(selectedKey, '');
    if (items.length > 1){
        let path = '';
        for(var j = 1; j < items.length; j++){
        var myEles = document.getElementsByTagName('li');
        for(var i=0; i < myEles.length; i++){
            if(myEles[i].innerHTML == items[j]){
            path += items[j] + '\\';
            const subkeys_ = await fetchSubkeys(items[0], path);
            toggleSubkeys(items[0], subkeys_, myEles[i], path);
            displayRegistryInfo(items[0], path);
            }
        }
        }
    }
    }
};

let root_ = null;
let selectedKey_ = null;
let old_name_ = null;

function resetOptions(){
    document.getElementById('create_key_box').style.display = 'none';
    document.getElementById('create_value_box').style.display = 'none';
    document.getElementById('rename_key_box').style.display = 'none';
    document.getElementById('search_value_box').style.display = 'none';
}

document.getElementById('yes_button').addEventListener('click', async (event) => {
    delete_reg_key();
    document.getElementById('confirm-delete').style.display = 'none';
    window.location.reload();
});

document.getElementById('no_button').addEventListener('click', async (event) => {
    document.getElementById('confirm-delete').style.display = 'none';
});

document.getElementById('close_button_confirm').addEventListener('click', async (event) => {
    document.getElementById('confirm-delete').style.display = 'none';
});

document.getElementById('create_reg_key').addEventListener('click', async (event) =>{
    resetOptions();
    document.getElementById('create_key_box').style.display = 'flex';
});

document.getElementById('create_reg_value').addEventListener('click', async (event) =>{
    resetOptions();
    document.getElementById('create_value_box').style.display = 'flex';
});

document.getElementById('rename_reg_key').addEventListener('click', async (event) =>{
    resetOptions();
    document.getElementById('rename_key_box').style.display = 'flex';
});

document.getElementById('search_reg_value').addEventListener('click', async (event) =>{
    resetOptions();
    document.getElementById('search_value_box').style.display = 'flex';
});

document.getElementById('delete_reg_key').addEventListener('click', async (event) => {
    resetOptions();
    document.getElementById('confirm-delete').style.display = 'block';
});

document.getElementById('search_value_button').addEventListener('click', async (event) =>{
    let name = document.getElementById('registry_value_name_search').value;
    path = await search_reg_value(name);
    if(path != null) {
    location_bar.value = path;
    update_url_cookie()
    const data = location_bar.value.split(/\\(.+)/);
    displayRegistryInfo(data[0], data[1]);
    }

});

document.getElementById('create_reg_button').addEventListener('click', async (event) =>{
    let name = document.getElementById('registry_key_name').value;
    create_reg_key(name);
    window.location.reload();
});

document.getElementById('create_value_button').addEventListener('click', async (event) =>{
    let name = document.getElementById('registry_value_name').value;
    let type = document.getElementById('registry_value_type').value;
    let value = document.getElementById('registry_value_data').value;
    create_reg_value(name, type, value);
    window.location.reload();
});

document.getElementById('rename_reg_button').addEventListener('click', async (event) =>{
    let name = document.getElementById('rename_key_name').value;
    rename_reg_key(name);
    window.location.reload();
});

document.getElementById('save_button').addEventListener('click', async (event) => {
    popup.style.display = 'none';

    valuebox = document.getElementById('value');
    valuebox.removeAttribute('disabled');

    namebox = document.getElementById('name');
    save_reg_info(root_, selectedKey_ , old_name_, namebox.value, valuebox.value);
});
document.getElementById('close_button').addEventListener('click', async (event) => {
    popup.style.display = 'none';
    document.getElementById('value').removeAttribute('disabled');
});

document.getElementById('delete_button').addEventListener('click', async (event) => {
    popup.style.display = 'none';
    document.getElementById('value').removeAttribute('disabled');

    delete_reg_value(root_, selectedKey_, old_name_);
    window.location.reload();
});

document.getElementById('cancel_button').addEventListener('click', async (event) => {
    popup.style.display = 'none';
    document.getElementById('value').removeAttribute('disabled');
});
rootList.oncontextmenu = disableRClickMenu;
rootList.addEventListener('click', async (event) => {
    if (event.target.classList.contains('root')) {
    const selectedKey = event.target.dataset.key;
    const rootElements = document.querySelectorAll('.root');
    rootElements.forEach(root => {
        root.classList.remove('active');
    });
    event.target.classList.add('active');
    location_bar.value = selectedKey;
    update_url_cookie();
    const subkeys = await fetchSubkeys(selectedKey, '');
    toggleSubkeys(selectedKey, subkeys, event.target, '');
    displayRegistryInfo(selectedKey, '')
    }
});
function toggleSubkeys(root, subkeys, rootKeyElement, previous_path) {
    const existingSublist = rootKeyElement.nextElementSibling;
    if (existingSublist && existingSublist.classList.contains('sublist')) {
        existingSublist.classList.toggle('active');
    } else {
        const subkeysList = document.createElement('ul');
        subkeysList.classList.add('sublist');
        if(subkeys != null) {
        subkeys.forEach(subkey => {
        const listItem = document.createElement('li');
        listItem.textContent = subkey;
        listItem.classList.add('sublist-item');
        listItem.oncontextmenu = disableRClickMenu;
        listItem.addEventListener('click', async (event) => {
            var selectedKey = ''
            if(!rootKeyElement.classList.contains('root')){
                selectedKey = previous_path.concat("\\",subkey);
            } else {
                selectedKey = subkey
            }
            const subkeys = await fetchSubkeys(root, selectedKey);
            location_bar.value = root + '\\' + selectedKey;
            update_url_cookie();
            toggleSubkeys(root, subkeys, event.target, selectedKey);
            displayRegistryInfo(root, selectedKey)
        });

        subkeysList.appendChild(listItem);
        });

        rootKeyElement.insertAdjacentElement('afterend', subkeysList);
        subkeysList.classList.add('active');
    }
    }
    }

    //////////////////////////// REGISTRY ////////////////////////////

async function displayRegistryInfo(root, selectedKey) {
    const registryInfo = await fetchRegistryInfo(root, selectedKey);

    var table = document.getElementById("registry-table").getElementsByTagName('tbody')[0];
    table.innerHTML = "";

    if(registryInfo != null) {
        registryInfo.forEach(([name, type, value]) => {

            if (type == "REG_BINARY"){
                const textEncoder = new TextEncoder();
                value = textEncoder.encode(value);
                value = Array.from(value, byte => byte.toString(16).padStart(2,'0')).join(' ');
            }

            addEntry(name, type, value).addEventListener('click', async (event) => {
            popup.style.display = 'block';
            document.getElementById('name').value = name
            let valuebox = document.getElementById('value')
            valuebox.value = value
            if(type != "REG_SZ"){
                valuebox.setAttribute('disabled', '');
            }

            root_ = root;
            selectedKey_ = selectedKey;
            old_name_ = name;

            });
        });
    }
}

    ////////////////////////////////////////  POPUP   ////////////////////////////////////////////////////

dragElement(document.getElementById("popup-edit"));

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function disableRClickMenu(clickEvent) { 
    clickEvent.preventDefault(); 
} 

function addEntry(name = '', type = '', value = '') {
    var table = document.getElementById("registry-table").getElementsByTagName('tbody')[0];
    var registry = table.insertRow(table.rows.length);

    var name_cell = registry.insertCell(0);
    var type_cell = registry.insertCell(1);
    var value_cell = registry.insertCell(2);

    name_cell.innerHTML = name;
    type_cell.innerHTML = type;
    value_cell.innerHTML = value;

    return registry;
}

    /////////////////////////////////////////////////////////////////////////////
    //FUNCTII PT REQUESTURI

async function fetchSubkeys(root, selectedKey) {
    const response = await fetch('/get_subkeys', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: root, key: selectedKey })
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to fetch subkeys');
        return [];
    }
}


async function fetchRegistryInfo(root, selectedKey) {
    const response = await fetch('/get_registry_info', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: root, key: selectedKey })
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to fetch registry info');
        return [];
    }
}


async function save_reg_info(root, selectedKey, old_name_, new_name_, new_value_) {
    const response = await fetch('/rename_reg_value', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: root, selected_key: selectedKey, new_name: new_name_, old_name: old_name_, new_value: new_value_})
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function create_reg_key(name) {

    const data = location_bar.value.split(/\\(.+)/);

    const response = await fetch('/create_reg_key', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: data[0], selected_key: data[1], name: name})
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function search_reg_value(name) {

    const data = location_bar.value.split(/\\(.+)/);

    const response = await fetch('/search_reg_value', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: data[0], path: data[1], name: name})
    });
    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function create_reg_value(name, type, value) {

    const data = location_bar.value.split(/\\(.+)/);

    if(type == 'REG_MULTI_SZ'){
        value = value.split(' ');
    }

    const response = await fetch('/create_reg_value', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: data[0], path: data[1], name: name, type: type, value: value})
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
} 

async function rename_reg_key(name) {

    const data = location_bar.value.split(/\\(.+)/);
    const items = data[1].split('\\');
    location_bar.value = location_bar.value.replace(items[items.length - 1], name);
    update_url_cookie();
    
    const response = await fetch('/rename_reg_key', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: data[0], old_key: data[1], name: name})
    });
    
    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}


async function delete_reg_value(root, selectedKey, value_name) {
    const response = await fetch('/delete_reg_value', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: root, selected_key: selectedKey, value_name: value_name})
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function delete_reg_key() {

    const data = location_bar.value.split(/\\(.+)/);
    const items = data[1].split('\\');
    location_bar.value = location_bar.value.replace('\\\\' + items[items.length - 1], '');
    update_url_cookie();

    const response = await fetch('/delete_reg_key', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ root: data[0], selected_key: data[1]})
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function update_url_cookie() {

    const response = await fetch('/set_url', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: location_bar.value})
    });

    if (response.ok) {
        const data = await response;
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}

async function get_url_cookie() {

    const response = await fetch('/get_url', {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to save registry info');
        return [];
    }
}
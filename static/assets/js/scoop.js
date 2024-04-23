var fileContents = {"rmlText":[], "owlText":[], "xsdText":[]};

function xsdLoadExample(exampleName) {

    if (exampleName) {

        var filePath = "examples/" + exampleName;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("xsdText").value = this.responseText;
            }
        };
        xhttp.open("GET", filePath, true);
        xhttp.send();
    } else {

        // document.getElementById("xsdText").value = "";
    }
}

function rmlLoadExample(exampleName) {

    if (exampleName) {

        var filePath = "examples/" + exampleName;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("rmlText").value = this.responseText;
            }
        };
        xhttp.open("GET", filePath, true);
        xhttp.send();
    } else {

        // document.getElementById("rmlText").value = "";
    }
}

function owlLoadExample(exampleName) {

    if (exampleName) {

        var filePath = "examples/" + exampleName;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("owlText").value = this.responseText;
            }
        };
        xhttp.open("GET", filePath, true);
        xhttp.send();
    } else {

        // document.getElementById("owlText").value = "";
    }
}

function shacl1LoadExample(exampleName) {

    if (exampleName) {

        var filePath = "examples/" + exampleName;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("shacl1Text").value = this.responseText;
            }
        };
        xhttp.open("GET", filePath, true);
        xhttp.send();
    } else {

        document.getElementById("shacl1Text").value = "";
    }
}

function shacl2LoadExample(exampleName) {

    if (exampleName) {

        var filePath = "examples/" + exampleName;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("shacl2Text").value = this.responseText;
            }
        };
        xhttp.open("GET", filePath, true);
        xhttp.send();
    } else {

        document.getElementById("shacl2Text").value = "";
    }
}

// function handleFileUpload(input) {
//     const file = input.files[0];
//     const reader = new FileReader();
//     reader.onload = function(e) {
//         const textAreaId = input.id.replace('File', '');
//         document.getElementById(textAreaId).value = e.target.result;
//     }
//     reader.readAsText(file);
// }



function handleFileUpload(input) {
    const files = input.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        reader.onload = function(e) {
            const textAreaId = input.id.replace('File', '');
            fileContents[textAreaId].push(e.target.result);
            // console.log('Current data:', fileContents[textAreaId]);
        }
        reader.readAsText(file);
    }
}

// function clearTextArea(textAreaId) {
//     document.getElementById(textAreaId).value = '';
// }
function clearTextArea(textAreaId) {
    document.getElementById(textAreaId).value = '';
    fileContents[textAreaId] = [];
    var fileInputId = textAreaId.replace('Text', 'TextFile');
    var fileInput = document.getElementById(fileInputId);
    if (fileInput) {
        fileInput.value = ''; 
        if (fileInput.files.length > 0) {
            fileInput.files = []; 
        }
    }
}

function downloadShaclOutput(shaclid) {
    var blob = new Blob([document.getElementById(shaclid).value], { type: 'text/turtle' });

    var downloadLink = document.createElement('a');
    downloadLink.href = window.URL.createObjectURL(blob);
    downloadLink.download = 'shacl.ttl'; 
    downloadLink.click();
}


const loadingSpinner = document.getElementById('loadingSpinner');

function translateIt() {
    document.getElementById('shaclOutput').innerText = '';
    document.getElementById('shaclOutput').style.color = 'black';
    var selectedOptions = document.querySelectorAll('input[name="mode"]:checked');
    var priorityOrder = Array.from(document.querySelectorAll('.priorityButton')).map(function(button) {
        return button.id;
    });
   
    if (document.getElementById('rmlText').value.trim() !== "") {
        fileContents['rmlText'].push(document.getElementById('rmlText').value);
    }
    
    if (document.getElementById('owlText').value.trim() !== "") {
        fileContents['owlText'].push(document.getElementById('owlText').value);
    }
    
    if (document.getElementById('xsdText').value.trim() !== "") {
        fileContents['xsdText'].push(document.getElementById('xsdText').value);
    }
    

    var requestData = {
        rmlData: fileContents['rmlText'],
        owlData: fileContents['owlText'],
        xsdData: fileContents['xsdText'],
        mode: selectedOptions[0].value, 
        priority: priorityOrder.join(' ')
    };
    
    var isEmpty = requestData.rmlData.length === 0 && requestData.owlData.length === 0 && requestData.xsdData.length === 0;
    
    if (isEmpty) {
        document.getElementById('shaclOutput').style.color = 'red';
        document.getElementById('shaclOutput').innerText = 'Please input data before translating!';
    } else {
        loadingSpinner.style.display = 'block';
        fetch('/translate', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(requestData) 
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('shaclOutput').value = data.shacl_output;
            loadingSpinner.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.style.display = 'none';
        });
    }
}


const loadingSpinner_integ = document.getElementById('loadingSpinner_integ');

function integrateIt() {
    loadingSpinner_integ.style.display = 'block';
    var selectedOption_integ = document.querySelector('input[name="mode_integ"]:checked').value;
    var requestData = {
        shacl1Data: document.getElementById('shacl1Text').value,
        shacl2Data: document.getElementById('shacl2Text').value,
        mode: selectedOption_integ
    };
    // console.log('Request data:', requestData);
    fetch('/integrate', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(requestData) 
    })
    .then(response => response.json())
    .then(data => {
        // console.log('Success:', data.shacl_output_integ);
        document.getElementById('shaclOutput_integ').value = data.shacl_output_integ;
        loadingSpinner_integ.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        loadingSpinner_integ.style.display = 'none';
    });   
}



const settingsIcon = document.getElementById('settingsIcon');
const settingsModal = document.getElementById('settingsModal');
const closeButton = document.getElementsByClassName('close')[0];
const saveButton = document.getElementById('saveButton');

settingsIcon.onclick = function() {
  settingsModal.style.display = 'block';
}

closeButton.onclick = function() {
  settingsModal.style.display = 'none';
}

saveButton.onclick = function() {

  settingsModal.style.display = 'none';
}


window.onclick = function(event) {
  if (event.target == settingsModal) {
    settingsModal.style.display = 'none';
  }
}



const settingsIcon_integ = document.getElementById('settingsIcon_integ');
const settingsModal_integ = document.getElementById('settingsModal_integ');
const closeButton_integ = document.getElementsByClassName('close_integ')[0];
const saveButton_integ = document.getElementById('saveButton_integ');

settingsIcon_integ.onclick = function() {
  settingsModal_integ.style.display = 'block';
}

closeButton_integ.onclick = function() {
  settingsModal_integ.style.display = 'none';
}

saveButton_integ.onclick = function() {

  settingsModal_integ.style.display = 'none';
}


window.onclick = function(event) {
  if (event.target == settingsModal_integ) {
    settingsModal_integ.style.display = 'none';
  }
}

// priority 
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var draggedButton = document.getElementById(data);
    var targetButton = ev.target.closest('.priorityOption').querySelector('.priorityButton');
    var targetIndex = Array.from(targetButton.parentNode.children).indexOf(targetButton);
    var draggedIndex = Array.from(draggedButton.parentNode.children).indexOf(draggedButton);

    if (draggedIndex < targetIndex) {
        targetButton.parentNode.insertBefore(draggedButton, targetButton.nextSibling);
    } else {
        targetButton.parentNode.insertBefore(draggedButton, targetButton);
    }
}

document.getElementById('priorityOptions').style.display = 'none';
document.getElementById('priorityROptions').style.display = 'none';

if (document.getElementById('priority').checked) {
    document.getElementById('priorityOptions').style.display = 'flex';
} else if (document.getElementById('priority-r').checked) {
    document.getElementById('priorityROptions').style.display = 'flex';
}

document.getElementById('priority').addEventListener('change', function() {
    document.getElementById('priorityOptions').style.display = this.checked ? 'flex' : 'none';
    document.getElementById('priorityROptions').style.display = 'none'; 
});

document.getElementById('priority-r').addEventListener('change', function() {
    document.getElementById('priorityROptions').style.display = this.checked ? 'flex' : 'none';
    document.getElementById('priorityOptions').style.display = 'none'; 
});


document.getElementById('saveButton').addEventListener('click', function() {
    var priorityOrder = Array.from(document.querySelectorAll('.priorityButton')).map(function(button) {
        return button.id;
    });
    console.log('Priority Order:', priorityOrder);
    // Send priorityOrder to backend
});
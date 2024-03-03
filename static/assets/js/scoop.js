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

        document.getElementById("xsdText").value = "";
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

        document.getElementById("rmlText").value = "";
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

        document.getElementById("owlText").value = "";
    }
}

function handleFileUpload(input) {
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const textAreaId = input.id.replace('File', '');
        document.getElementById(textAreaId).value = e.target.result;
    }
    reader.readAsText(file);
}


function translateIt() {

    var selectedOption = document.querySelector('input[name="mode"]:checked').value;
    var requestData = {
        rmlData: document.getElementById('rmlText').value,
        owlData: document.getElementById('owlText').value,
        xsdData: document.getElementById('xsdText').value,
        mode: selectedOption
    };

    fetch('/translate', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(requestData) 
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data.shacl_output);
        document.getElementById('shaclOutput').value = data.shacl_output;
    })
    .catch(error => {
        console.error('Error:', error);
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
  const checkboxChecked = document.getElementById('checkbox').checked;
  const prioritySelected = document.querySelector('input[name="mode"]:checked').value;

  console.log('Checkbox checked:', checkboxChecked);
  console.log('Priority selected:', prioritySelected);

  settingsModal.style.display = 'none';
}

// 当用户点击弹窗外部区域时关闭弹窗
window.onclick = function(event) {
  if (event.target == settingsModal) {
    settingsModal.style.display = 'none';
  }
}

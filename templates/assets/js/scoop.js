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

// function translateIt() {

//     var formData = new FormData();
//     formData.append('xsdData', document.getElementById('xsdText').value);       
//     formData.append('rmlData', document.getElementById('rmlText').value);
//     formData.append('owlData', document.getElementById('owlText').value);

//     // Send POST request to backend
//     fetch('/translate', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Handle the response from backend
//         console.log('SHACL output:', data);
//         // document.getElementById('shaclOutput').innerText = JSON.stringify(data, null, 2);
//         document.getElementById('shaclOutput').innerText = data.shacl_output;
//         // Update your HTML elements with the SHACL output
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });   
// } 
function translateIt() {

    var requestData = {
        rmlData: document.getElementById('rmlText').value,
        owlData: document.getElementById('owlText').value,
        xsdData: document.getElementById('xsdText').value
    };


    fetch('https://good-gray-caterpillar-robe.cyclic.app/translate', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(requestData) 
    })
    .then(response => response.json())
    .then(data => {

        console.log('SHACL output:', data);
        document.getElementById('shaclOutput').innerText = data.shacl_output;

    })
    .catch(error => {
        console.error('Error:', error);
    });   
}

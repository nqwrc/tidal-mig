document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let fileInput = document.getElementById('csvFile');
    let file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('csvFile', file);

        fetch('/import_favorites', {
            method: 'POST',
            body: formData 
        })
        .then(response => response.text()) 
        .then(result => { 
            console.log('Import Result:', result); 
            // Display a success or error message to the user
        })
        .catch(error => console.error('Import Error:', error));

        let reader = new FileReader();
        reader.onload = function(e) {
            let csvData = e.target.result;
        }   
        reader.readAsText(file);
    }
});


const downloadButtons = document.querySelectorAll('.download-csv');
downloadButtons.forEach(button => {
    button.addEventListener('click', handleCSVDownload);
});

function handleCSVDownload(event) {
    const link = document.createElement('a');

    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); 
}
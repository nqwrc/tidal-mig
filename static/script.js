// Function to handle login
function handleLogin() {
  fetch('/login', {
    method: 'POST'
  })
  .then(response => {
    if (response.ok) {
      window.location.href = '/post_login';
    } else {
      console.error('Could not connect to Tidal');
    }
  })
  .catch(error => console.error(error));
}

// Show the selected category view and hide the category selection
function showCategory(category) {
  document.getElementById("categorySelection").style.display = "none";
  var views = document.getElementsByClassName("category-view");
  for (var i = 0; i < views.length; i++) {
    views[i].style.display = "none";
  }
  document.getElementById(category + "View").style.display = "block";
}

// Return to the main category selection
function backToCategories() {
  var views = document.getElementsByClassName("category-view");
  for (var i = 0; i < views.length; i++) {
    views[i].style.display = "none";
  }
  document.getElementById("categorySelection").style.display = "block";
}

// CSV File Upload handling
document.getElementById('uploadForm')?.addEventListener('submit', function(e) {
  e.preventDefault();
  const csvInput = document.getElementById('csvFile');
  const file = csvInput.files[0];

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
      // Optionally, display a success or error message.
    })
    .catch(error => console.error('Import Error:', error));

    const reader = new FileReader();
    reader.onload = function(e) {
      const csvData = e.target.result;
      // Optionally process CSV data here.
    }
    reader.readAsText(file);
  }
});

// CSV Download handling
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

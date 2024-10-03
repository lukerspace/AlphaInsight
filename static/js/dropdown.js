


const dropdownList = () => {
    // Wait for 0.5 seconds before executing the code inside setTimeout
    setTimeout(() => {
      // Get the dropdown element
      const dropdown = document.getElementById('headingDropdown');
  
      // Fetch data from the API
      fetch(`${window.origin}/api/user/strategy`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          // Clear previous options
          dropdown.innerHTML = '';
          console.log(data)
  
          // Populate the dropdown with fetched data
          data["dropdown_list"].forEach(strategy => {
            const option = document.createElement('option');
            option.textContent = strategy; // Assuming strategy object has a 'name' property
            dropdown.appendChild(option);
          });
          // Trigger the dropdown change event after fetch is complete
          dropdown.dispatchEvent(new Event('change'));
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    }, 500); // 500 milliseconds = 0.5 seconds
  
  
  
  // Event listener for dropdown change event
  document.getElementById('headingDropdown').addEventListener('change', (event) => {
      // Get the selected option text content
      const selectedOptionText = event.target.selectedOptions[0].textContent;
      // Generate a unique ID based on the selected option text content
      const uniqueId = 'strategy';
      // Set the unique ID to the selected option
      event.target.selectedOptions[0].id = uniqueId;
      const optionstag = event.target.options;
      for (let i = 0; i < optionstag.length; i++) {
          if (optionstag[i] !== event.target.selectedOptions[0]) {
            optionstag[i].removeAttribute('id');
          }}
    });
  };
  



document.addEventListener('DOMContentLoaded', function () {
    const apiUrl = '/api/coppock_data'; // Replace this with your actual API URL
    const tableExample2 = document.getElementById('example2').getElementsByTagName('tbody')[0];

    // Function to fetch API data
    async function fetchCoppockData() {
        try {
            const response = await fetch(apiUrl);
            const data = await response.json();
            populateTable(data);
        } catch (error) {
            console.error('Error fetching Coppock data:', error);
        }
    }

    // Function to dynamically populate the table with data
    function populateTable(data) {
        const assetOrder = ['XLK', 'XLY', 'XLI', 'XLP', 'XLF', 'XLE', 'XLU', 'XLRE', 'XLC', 'XLV', 'XLB', 'SPY'];

        // Clear previous rows (if any)
        tableExample2.innerHTML = '';

        // Loop through the API data and create table rows and cells dynamically
        Object.entries(data).forEach(([date, values], index) => {
            // Create a new table row
            const row = document.createElement('tr');

            // Create and append the date cell
            const dateCell = document.createElement('td');
            dateCell.textContent = date.split(' ')[0]; // Show only the date part
            row.appendChild(dateCell);

            // Loop through each asset value and create cells for them
            values.forEach((value, assetIndex) => {
                const cell = document.createElement('td');
                cell.textContent = value.toFixed(2); // Format to 2 decimal places
                row.appendChild(cell); // Append the cell to the row
            });

            // Append the created row to the table
            tableExample2.appendChild(row);
            
        })
        decorateTable();
    }

    // Fetch and populate the table
    fetchCoppockData();
    
    // Function to decorate the table using DataTables
    function decorateTable() {
        $('#example2').DataTable({
          paging: false,
          searching: false,
          info: false,
        //   pageLength: 2,      // Show 50 rows per page
        //   lengthMenu: [2, 3, 50, 500],
          ordering: false,// Set number of rows per page
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const apiUrl = '/api/coppock_ratio';  // Replace with your actual API URL
    const tableExample3 = document.getElementById('example3').getElementsByTagName('tbody')[0];

    // Asset order corresponding to the table columns
    const assetKeys = ['XLK', 'XLY', 'XLI', 'XLP', 'XLF', 'XLE', 'XLU', 'XLRE', 'XLC', 'XLV', 'XLB', 'SPY', 'TLT'];

    // Function to fetch API data
    const fetchCoppockData = async () => {
        try {
            const response = await fetch(apiUrl);
            const data = await response.json();
            populateTable(data);
        } catch (error) {
            console.error('Error fetching Coppock data:', error);
        }
    };

    // Function to dynamically populate the table with data
    const populateTable = data => {
        // Clear previous rows (if any)
        tableExample3.innerHTML = '';

        // Loop through the API data and create table rows and cells dynamically
        Object.entries(data).forEach(([date, values], index) => {
            // Limit to 3 rows
            if (index < 3) {
                // Create a new table row
                const row = document.createElement('tr');

                // Create and append the date cell
                const dateCell = document.createElement('td');
                dateCell.textContent = date.split(' ')[0]; // Show only the date part
                row.appendChild(dateCell);

                // Loop through each asset value and create cells for them
                values.forEach((value, assetIndex) => {
                    const cell = document.createElement('td');
                    cell.textContent = value.toFixed(2); // Format to 2 decimal places
                    row.appendChild(cell); // Append the cell to the row
                });

                // Append the created row to the table
                tableExample3.appendChild(row);
            }
        });
        decorateTable()
    };

    // Fetch and populate the table
    fetchCoppockData();
    
    // Function to decorate the table using DataTables
    function decorateTable() {
        $('#example3').DataTable({
          paging: false,
          searching: false,
          info: false,
        //   pageLength: 5, 
          ordering: false, // Set number of rows per page
        });
    }
});

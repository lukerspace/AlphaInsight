    // Function to populate the table
    function fetchStartDate() {
        fetch('/api/daily') // Assuming the API provides a route to get the first item by ID
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // console.log(data[0]["created_at"])
                // Display the created_at date in the div with id="startdate"
                document.getElementById('startdate').textContent = `Date: ${data[0].created_at}`;
            })
            .catch(error => {
                console.error('Error fetching start date:', error);
            });
    }
    function populateTable(data) {
        const tableBody = document.querySelector('#example4 tbody');
        tableBody.innerHTML = ''; // Clear previous table data
        data.forEach(item => {
            const row = `
                <tr>
                    <td>${item.ticker}</td>
                    <td>${item.daily_change}</td>
                    <td>${item.week_change}</td>
                    <td>${item.bi_weekly_change}</td>
                    <td>${item.monthly_change}</td>
                    <td>${item.quarterly_change}</td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });
        $(document).ready(function() {
            $('#example4').DataTable({
                "paging": true,
                "pageLength":10,
                "searching": true,
                "ordering": false,
                "info": false,
                "order": [[2, "desc"]]  // Order by the Weekly column (index 2) in descending order
            
            });
        })
    }

    // Fetch data from /api/data route
    function fetchData() {
        fetch('/api/daily')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                populateTable(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });

    }

    // Populate the table on page load
    document.addEventListener('DOMContentLoaded', function() {
        fetchData();
        fetchStartDate();
        
    });




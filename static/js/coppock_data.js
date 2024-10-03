document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = '/api/coppock_data';  // Replace this with your actual API URL

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

    // Function to populate the table with data
    function populateTable(data) {
        const ids = [
            { date: 'date1', xlk: 'xlk1', xly: 'xly1', xli: 'xli1', xlp: 'xlp1', xlf: 'xlf1', xle: 'xle1', xlu: 'xlu1', xlre: 'xlre1', xlc: 'xlc1', xlv: 'xlv1', xlb: 'xlb1', spy: 'spy1', },
            { date: 'date2', xlk: 'xlk2', xly: 'xly2', xli: 'xli2', xlp: 'xlp2', xlf: 'xlf2', xle: 'xle2', xlu: 'xlu2', xlre: 'xlre2', xlc: 'xlc2', xlv: 'xlv2', xlb: 'xlb2', spy: 'spy2', },
            { date: 'date3', xlk: 'xlk3', xly: 'xly3', xli: 'xli3', xlp: 'xlp3', xlf: 'xlf3', xle: 'xle3', xlu: 'xlu3', xlre: 'xlre3', xlc: 'xlc3', xlv: 'xlv3', xlb: 'xlb3', spy: 'spy3', }
        ];

        const assetOrder = ['XLK', 'XLY', 'XLI', 'XLP', 'XLF', 'XLE', 'XLU', 'XLRE', 'XLC', 'XLV', 'XLB', 'SPY'];

        const dateEntries = Object.entries(data);
        
        // Loop through each entry in the API data and each row in the table
        dateEntries.forEach((entry, index) => {
            const [date, values] = entry;
            
            // Make sure not to exceed the predefined rows
            if (index < ids.length) {
                document.getElementById(ids[index].date).textContent = date.split(' ')[0]; // Only show the date part

                // Loop through the asset values and populate each cell
                values.forEach((value, idx) => {
                    const assetId = ids[index][assetOrder[idx].toLowerCase()];  // Get the ID based on the asset order
                    document.getElementById(assetId).textContent = value.toFixed(2);  // Format the value to 2 decimal places
                });
            }
        });
    }

    // Fetch and populate the table
    fetchCoppockData();
});


document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = '/api/coppock_ratio';  // Replace with your actual API URL

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

    // Function to populate the table with data
    const populateTable = data => {
        Object.entries(data).forEach(([date, values], index) => {
            // Limit to 3 rows
            if (index < 3) {
                document.getElementById(`rdate${index + 1}`).textContent = date.split(' ')[0];  // Date column

                // Populate asset columns
                values.forEach((value, assetIndex) => {
                    const assetId = `r${assetKeys[assetIndex].toLowerCase()}${index + 1}`;
                    document.getElementById(assetId).textContent = value.toFixed(2);
                });
            }
        });
    };

    // Fetch and populate the table
    fetchCoppockData();
});
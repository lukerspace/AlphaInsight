// Function
const fetchData =(strategyname,year,month)=>{
  console.log("Verifying")
  let xaxisDate;
  let benchmarkValue;
  let strategyValue;
  let benchmarkValueHold
  let strategyValueHold
  if (token && new Date().getTime() < tokenExpiration) {
    console.log(token && new Date().getTime())
    // console.log(tokenExpiration)
    // console.log("token time usable:",token && new Date().getTime()<tokenExpiration)

    fetch(`${window.origin}/api/nav?graphname=${strategyname}&year=${year}&month=${month}`, {
        method: "GET",
        headers: new Headers({
          "Content-Type": "application/json",
        }),
      })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then((ressponse_data) => {

        //  chart from echart 
        data=ressponse_data["data"]
        xaxisDate = data["Date"];
        benchmarkValue = data["Benchmarkvalue"];
        strategyValue = data["Strategyvalue"];
        benchmarkValueHold = data["BenchmarkvalueHold"];
        strategyValueHold = data["StrategyvalueHold"];

        var chartDom = document.getElementById('main');
        var chartDom2= document.getElementById('bh')
        var myChart = echarts.init(chartDom);
        var myChart2 = echarts.init(chartDom2);
        var option;
        var option2;

        option = {
          title: {
            text: 'Return in Percentage %'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: [ 'benchmark', 'strategy']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xaxisDate
          },
          yAxis: {
            type: 'value'
          },
          color: ['#1E90FF', '#800080'],
          series: [
            {
              name: 'benchmark',
              type: 'line',
              lineStyle: {
                width: 3 // Set line width to 3
              },

              data: benchmarkValue
            },
            {
              name: 'strategy',
              type: 'line',
              lineStyle: {
                width: 3 // Set line width to 3
              },

              data: strategyValue
            }
          ]
        };

        option2={
          title: {
            text: 'B&H Return from Different Start Dates'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: [ 'benchmark', 'strategy']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xaxisDate
          },
          yAxis: {
            type: 'value'
          },
          color: ['orange', '#006400'],
          series: [
            {
              name: 'benchmark',
              type: 'line',
              lineStyle: {
                width: 3 // Set line width to 3
              },

              data: benchmarkValueHold
            },
            {
              name: 'strategy',
              type: 'line',
              lineStyle: {
                width: 3 // Set line width to 3
              },

              data: strategyValueHold
            }
          ]
        }

        option && myChart.setOption(option);
        option2 && myChart2.setOption(option2);

        // performance table
        var strategytablereview
        var benchmarktablereview
        strategytablereview=(ressponse_data["metrics"]["strategy"])
        benchmarktablereview=(ressponse_data["metrics"]["benchmark"])
        // console.log(benchmarktablereview)
        // console.log(strategytablereview)
        renderMericTable(strategytablereview,benchmarktablereview)
      })
      .catch((error) => {
        console.error('There was a problem with ECHART :', error);
        // alert("Error on fetch operation")
      })
  }else {
    // Clear token and token expiration
    localStorage.removeItem('token');
    localStorage.removeItem('tokenExpiration');
    // localStorage.removeItem('signoutTriggered');

    // Ensure this only triggers once
    if (!localStorage.getItem('signoutTriggered')) {
        localStorage.setItem('signoutTriggered', 'true');
        // Show alert and handle signout

        // 
        console.log("Log Out / Token Expired");

        // Reload the page after the signout process is triggered
        setTimeout(() => {
            // Reset the flag to allow future signouts
            localStorage.setItem('signoutTriggered',"false");
            window.location.reload();
        }, 300);
        document.getElementById('logOut').click();
    }
    if (localStorage.getItem('signoutTriggered')=="false") {
      localStorage.removeItem('signoutTriggered')
  
    }
  }
};

const selectDate=()=> {
  const year = document.getElementById("year").value;
  const month = document.getElementById("month").value;
  const strategyname=document.getElementById("strategy").value;

  // Check if both year and month are selected
  if (year !== "0" && month !== "0") {
    const yyyymm = year + month.padStart(2, '0');
    console.log(yyyymm)
    fetchData(strategyname,year, month);

  } else {
    alert("Please select both year and month.");
  }
}

const populateDays=()=> {
  const month = document.getElementById("month").value;
  const year = document.getElementById("year").value;
  // Get the number of days in the selected month
  const daysInMonth = new Date(year, month, 0).getDate();
  // Populate days dropdown with options
  for (let i = 1; i <= daysInMonth; i++) {
    const option = document.createElement("option");
    option.text = i;
    option.value = i;
  }
}

const populateYears=()=> {
  const yearsDropdown = document.getElementById("year");
  const currentYear = new Date().getFullYear();
  // Clear previous options
  yearsDropdown.innerHTML = "<option value='0'>Year</option>";
  // Populate years dropdown with options for the past 17 years
  for (let i = currentYear; i >= currentYear - 17; i--) {
    const option = document.createElement("option");
    option.text = i;
    option.value = i;
    yearsDropdown.add(option);
  }
}

const renderUpdateDate = () => {
  fetch(`${window.origin}/api/ivdelta`)
    .then(response => response.json())
    .then(data => {
      // Extract sysdate and find the latest one
      const update = data.map(item => new Date(item.sysdate));

      // Find the latest sysdate (most recent date)
      const latestSysdate = new Date(Math.max(...update));

      // Format the date in a readable format (adjust as needed)
      const formattedDate = `${latestSysdate.getFullYear()}-${latestSysdate.getMonth() + 1}-${latestSysdate.getDate()}`;

      // Render the latest date in the div with id="ivdate"
      document.getElementById('ivdate').innerText = `Latest Update: ${formattedDate}`;

      // console.log(`Latest Update : ${formattedDate}`);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
};

const renderMericTable =(strategytablereview,benchmarktablereview)=>{
  var asset1 = "Strategy";
  var asset2 = "Benchmark";
  // Get a reference to the table body
  var tableBody = document.querySelector("#mettable tbody");
  // Clear all existing rows (td) from the table body
  tableBody.innerHTML = ''; // 
  // Function to create a table row with the given asset name and data
  function createTableRow(assetName, reviewData) {
      var row = document.createElement("tr");
      // Create and append the columns for each row
      var assetCell = document.createElement("td");
      assetCell.textContent = assetName;
      row.appendChild(assetCell);
      var returnCell = document.createElement("td");
      returnCell.textContent = reviewData["Return %"];
      row.appendChild(returnCell);
      var annualReturnCell = document.createElement("td");
      annualReturnCell.textContent = reviewData["Comp. Annual Return"];
      row.appendChild(annualReturnCell);

      var maxDrawdownCell = document.createElement("td");
      maxDrawdownCell.textContent = reviewData["Max Drawdown %"];
      row.appendChild(maxDrawdownCell);

      var maxDrawdownDateCell = document.createElement("td");
      maxDrawdownDateCell.textContent = new Date(reviewData["Max Drawdown % Date"]).toLocaleDateString();
      row.appendChild(maxDrawdownDateCell);

      var returnDrawdownRatioCell = document.createElement("td");
      returnDrawdownRatioCell.textContent = reviewData["Return%/Max Drawdown%"];
      row.appendChild(returnDrawdownRatioCell);

      var stdDevCell = document.createElement("td");
      stdDevCell.textContent = reviewData["Std"];
      row.appendChild(stdDevCell);

      var sharpeRatioCell = document.createElement("td");
      sharpeRatioCell.textContent = reviewData["Sharpe Ratio"];
      row.appendChild(sharpeRatioCell);

      var calmarRatioCell = document.createElement("td");
      calmarRatioCell.textContent = reviewData["Calmar Ratio"];
      row.appendChild(calmarRatioCell);
      return row;
  }

  // Create the rows for both the strategy and benchmark
  var strategyRow = createTableRow(asset1, strategytablereview);
  var benchmarkRow = createTableRow(asset2, benchmarktablereview);

  // Append the rows to the table body
  tableBody.appendChild(strategyRow);
  tableBody.appendChild(benchmarkRow);
  
  $(document).ready(function() {
    // Check if DataTable is already initialized
    if ($.fn.DataTable.isDataTable('#mettable')) {
        // If DataTable is initialized, just clear and redraw it
        $('#mettable').DataTable().clear();
    } else {
        // If DataTable is not initialized, initialize it
        $('#mettable').DataTable({
            "paging": false,
            "searching": false,
            "ordering": false,
            "info": false,
            "paging": false  // Optionally disable paging if height is limited
        });
      }
  });

  // Show the table if it was initially hidden
  // document.getElementById("mettable").classList.remove("hide");


}

const renderReturn=()=>{
  // Populate months dropdown &  Populate years dropdown on page load
  const monthsDropdown = document.getElementById("month");
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  for (let i = 0; i < months.length; i++) {
    const option = document.createElement("option");
    option.text = months[i];
    option.value = i+1;
    monthsDropdown.add(option);
  }// Event listeners to trigger population of days dropdown when month or year changes
  document.getElementById("month").addEventListener("change", populateDays);
  document.getElementById("year").addEventListener("change", populateDays);
  populateYears();


  // Set default year and month values
  const defaultstrategy="COPPOCK"
  const defaultYear = new Date().getFullYear()-1;
  const defaultMonth = new Date().getMonth()+1  ; // Month is zero-indexed, so we add 1 to get the correct month
  document.getElementById('year').value = defaultYear;
  document.getElementById('month').value = defaultMonth;
  // console.log(defaultYear,defaultMonth,defaultstrategy)
  fetchData(defaultstrategy,defaultYear, defaultMonth);
}

const renderIvDelta=()=>{
  fetch(`${window.origin}/api/ivdelta`)
  .then(response => response.json())
  .then(data => {
      // Extract the relevant data for the chart
      // Assuming API returns a list of objects with date, value, and delta
      const dates = data.map(item => item.date);    // X-axis: dates
      const values = data.map(item => item.value);  // Y-axis: values
      const deltas = data.map(item => item.delta);  // Secondary Y-axis: deltas (optional)

      // Initialize the ECharts instance
      const chart = echarts.init(document.getElementById('ivdelta'));

      // Specify the chart configuration
      const option = {
          title: {
              text: 'SPY IV 25% Delta Data'
          },
          tooltip: {
              trigger: 'axis'
          },
          xAxis: {
              type: 'category',
              data: dates,
              axisLabel: {
                  rotate: 45,  // Rotate labels if they overlap
                  formatter: function(value) {
                      // Format date if needed
                      const date = new Date(value);
                      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
                  }
              }
          },
          yAxis: [
              {
                  type: 'value',
                  name: 'Value',
                  min:500
              },
              {
                  type: 'value',
                  name: 'Delta',
                  position: 'right',
                  offset: 60  // Offset to the right to display the secondary axis
              }
          ],
          series: [
              {
                  name: 'Value',
                  type: 'line',
                  data: values,
                  smooth: true,
                  yAxisIndex: 0  // Link to the first Y-axis
              },
              {
                  name: 'Delta',
                  type: 'line',
                  data: deltas,
                  smooth: true,
                  yAxisIndex: 1,  // Link to the secondary Y-axis
                  lineStyle: {
                      type: 'dashed'  // Optional: make delta line dashed for distinction
                  }
              }
          ]
      };

      // Use the specified configuration and data to display the chart
      chart.setOption(option);
  })
  .catch(error => {
      console.error('Error fetching data:', error);
  });
}






// Check token validity and fetch data if valid
const token = localStorage.getItem('token');
const tokenExpiration = localStorage.getItem('tokenExpiration');
console.log('LocalStorage ',tokenExpiration)
renderReturn()
renderIvDelta()
renderUpdateDate()

// Add click event listener to the button
// Signout Redirect 
document.getElementById("logDateButton").addEventListener("click", selectDate);
if (localStorage.getItem('signoutTriggered')=="false") {
  localStorage.removeItem('signoutTriggered')
}
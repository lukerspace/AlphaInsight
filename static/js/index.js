// Function to fetch the data from mysql
const fetchData =(strategyname,year,month)=>{
  console.log("Verifying Token ..")
  
  let xaxisDate;
  let benchmarkValue;
  let strategyValue;
  if (token && new Date().getTime() < tokenExpiration) {
    console.log(token && new Date().getTime())
    console.log(tokenExpiration)
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
      .then((data) => {
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


// Function to log Selected Date
const logSelectedDate=()=> {
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


// Function to populate days dropdown based on selected month and year
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

// Function to populate years dropdown
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



// Check token validity and fetch data if valid
const token = localStorage.getItem('token');
const tokenExpiration = localStorage.getItem('tokenExpiration');
console.log('localstorage',token)
console.log('localstorage time',tokenExpiration)

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
const defaultstrategy="COT_COMMERCIAL"
const defaultYear = new Date().getFullYear()-1;
const defaultMonth = new Date().getMonth()+1  ; // Month is zero-indexed, so we add 1 to get the correct month
document.getElementById('year').value = defaultYear;
document.getElementById('month').value = defaultMonth;
console.log(defaultYear,defaultMonth,defaultstrategy)
fetchData(defaultstrategy,defaultYear, defaultMonth);

// Add click event listener to the button
document.getElementById("logDateButton").addEventListener("click", logSelectedDate);




if (localStorage.getItem('signoutTriggered')=="false") {
  localStorage.removeItem('signoutTriggered')
}
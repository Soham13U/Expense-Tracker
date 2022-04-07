const renderChart = (data, labels) => {
  const line=document.getElementById("line");
  const bar=document.getElementById("bar");
  
  const doughnut=document.getElementById("doughnut");
 
  const radar=document.getElementById("radar");
  const polarArea=document.getElementById("polarArea");
  

  line.addEventListener('click',changeline);
  bar.addEventListener('click',changebar);
 
  doughnut.addEventListener('click',changedoughnut);
  
  radar.addEventListener('click',changeradar);
  polarArea.addEventListener('click',changepolarArea);
  

    var ctx = document.getElementById("myChart").getContext("2d");
    var config =  {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last 6 months expenses",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Expenses per category",
        },
      },
    }

    var configLine={
      type: 'line',
      data:{
        labels: labels,
      datasets: [{
    label: 'Last 6 months expenses',
    data: data,
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
      },
      options:{}
    };

    var configBar={
      type: 'bar',
      data:{
        labels: labels,
  datasets: [{
    label: 'Last 6 months expenses',
    data:data,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    borderWidth: 1
  }]
      },
      options:{}
    };

    var configPolarArea={
      type: 'polarArea',
      data:{
        labels: labels,
        datasets: [{
          label: 'Last 6 months expenses',
          data:data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ]
        }] },
      options:{}
    };

    var configRadar={
      type: 'radar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months expenses',
          data: data,
          fill: true,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgb(255, 99, 132)',
          pointBackgroundColor: 'rgb(255, 99, 132)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(255, 99, 132)'
        },
      ]
      },
      options: {
        elements: {
          line: {
            borderWidth: 3
          }
        }
      },
      options:{}
    };

    

    

    var myChart = new Chart(ctx,config);
    function changeline(){
      // console.log(myChart2.config.type);
      myChart.destroy();
      myChart = new Chart(ctx,configLine);
      myChart.config.type='line';
      myChart.update();
  };
  function changebar(){
      // console.log(myChart2.config.type);
      myChart.destroy();
      myChart = new Chart(ctx,configBar);
      myChart.config.type='bar';
      myChart.update();
  };
 
function changedoughnut(){
    // console.log(myChart2.config.type);
    myChart.destroy();
    myChart = new Chart(ctx,config);
    myChart.config.type='doughnut';
    myChart.update();
};

function changepolarArea(){
  // console.log(myChart2.config.type);
  myChart.destroy();
    myChart = new Chart(ctx,configPolarArea);
  myChart.config.type='polarArea';
  myChart.update();
};
function changeradar(){
  // console.log(myChart2.config.type);
  myChart.destroy();
  myChart = new Chart(ctx,configRadar);
  myChart.config.type='radar';
  myChart.update();
};


  };
  
  const getChartData = () => {
    console.log("fetching");
    fetch("/expense_category_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_data = results.expense_category_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
  
        renderChart(data, labels);
      });
  };

  document.onload = getChartData();
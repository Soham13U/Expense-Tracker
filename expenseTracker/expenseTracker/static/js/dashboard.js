// const line=document.getElementById("line"),pie=document.getElementById("pie");
// let myChart1,myChart2,data_expense,labels_expense,label_title_expense,data_income,labels_income,label_title_income;
// line.addEventListener("click",()=>{myChart1.destroy(),myChart2.destroy(),renderExpenseChart(data_expense,labels_expense,"line",label_title_expense),renderIncomeChart(data_income,labels_income,"line",label_title_income)}),pie.addEventListener("click",()=>{myChart1.destroy(),myChart2.destroy(),renderExpenseChart(data_expense,labels_expense,"pie",label_title_expense),renderIncomeChart(data_income,labels_income,"pie",label_title_income)});const renderExpenseChart=(e,t,a,n)=>{var r=document.getElementById("myChart").getContext("2d");

// myChart1=new Chart(r,{type:a,data:{labels:t,datasets:[{label:"This month's expenses",data:e,backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(54, 162, 235, 0.2)","rgba(255, 206, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(153, 102, 255, 0.2)","rgba(255, 159, 64, 0.2)"],borderColor:["rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)","rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)","rgba(255, 159, 64, 1)"],borderWidth:1}]},options:{title:{display:!0,text:n}}})},renderIncomeChart=(e,t,a,n)=>{var r=document.getElementById("myChart2").getContext("2d");myChart2=new Chart(r,{type:a,data:{labels:t,datasets:[{label:"This month's incomes",data:e,backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(54, 162, 235, 0.2)","rgba(255, 206, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(153, 102, 255, 0.2)","rgba(255, 159, 64, 0.2)"],borderColor:["rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)","rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)","rgba(255, 159, 64, 1)"],borderWidth:1}]},options:{title:{display:!0,text:n}}})},getChartData=e=>{fetch("/expense_category_summary?filter=month").then(e=>e.json()).then(t=>{const a=t.expense_category_data;label_title_expense=t.label_title;
//     const[n,r]=[Object.keys(a),Object.values(a)];
    
//     renderExpenseChart(data_expense=r,labels_expense=n,e,label_title_expense)}),fetch("/income/income_source_summary?filter=month").then(e=>e.json()).then(t=>{const a=t.income_source_data;label_title_income=t.label_title;
//         const[n,r]=[Object.keys(a),Object.values(a)];
        
//         renderIncomeChart(data_income=r,labels_income=n,e,label_title_income)})};document.onload=getChartData("pie");






const renderChart = (data, labels) => {
  const line=document.getElementById("line");
const bar=document.getElementById("bar");


line.addEventListener('click',changeline);
bar.addEventListener('click',changebar);
  var ctx = document.getElementById("myChart1").getContext("2d");
  var myChart1 = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total expenses",
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
  });
  function changeline(){
      // console.log(myChart1.config.type);
      myChart1.config.type='line';
      myChart1.update();
  };
  function changebar(){
      // console.log(myChart1.config.type);
      myChart1.config.type='bar';
      myChart1.update();
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


const renderChart2 = (data, labels) => {
  const line=document.getElementById("line");
  const bar=document.getElementById("bar");
  
  line.addEventListener('click',changeline);
  bar.addEventListener('click',changebar);
  var ctx = document.getElementById("myChart2").getContext("2d");
  var myChart2 = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total income",
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
        text: "Income per category",
      },
    },
  });
  function changeline(){
      // console.log(myChart2.config.type);
      myChart2.config.type='line';
      myChart2.update();
  };
  function changebar(){
      // console.log(myChart2.config.type);
      myChart2.config.type='bar';
      myChart2.update();
  };
};

const getChartData2 = () => {
  console.log("fetching");
  fetch('/income/income_source_summary')
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const source_data = results.income_source_data;
      const [labels, data] = [
        Object.keys(source_data),
        Object.values(source_data),
      ];

      renderChart2(data, labels);
    });
};

document.onload = getChartData2();       




const renderChart3 = () => {
  const line=document.getElementById("line");
  const bar=document.getElementById("bar");
  
  line.addEventListener('click',changeline);
  bar.addEventListener('click',changebar);
  var ctx = document.getElementById("myChart3").getContext("2d");
  var myChart3 = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Expense','Income'],
      datasets: [
        {
          // label: "Total income",
          data: [valS,valE],
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
        text: "Income per category",
      },
      scales:{
        yAxes: [{
          ticks: {
            reverse: false,
            min:0,
            max:100000,

            stepSize: 5000
          },
        }]

      },
    },
  });
  function changeline(){
      // console.log(myChart2.config.type);
      myChart3.config.type='line';
      myChart3.update();
  };
  function changebar(){
      // console.log(myChart2.config.type);
      myChart3.config.type='bar';
      myChart3.update();
  };
};

// const getChartData3 = () => {
//   console.log("fetching");
//   fetch('/income/income_source_summary')
//     .then((res) => res.json())
//     .then((results) => {
//       console.log("results", results);
//       const source_data = results.income_source_data;
//       const [labels, data] = [
//         Object.keys(source_data),
//         Object.values(source_data),
//       ];

//       renderChart3(data, labels);
//     });
// };
renderChart3();
// document.onload = getChartData3();       





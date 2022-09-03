var line_chart = false
var pie_chart = false
var global_timeframe

function load_chart(timeframe){
    if (line_chart != false){ // if chart instance exists
        line_chart.destroy()
    }
    global_timeframe = timeframe
    $.ajax({
        url:"http://127.0.0.1:8000/api/portfolio/historical/?username=0xd2b101d3a69b20ac140ce233a67dd88abb0222b1",
        type:"GET",
        dataType:"json",
        success: function(data){
            console.log(data["message"])
            // ref https://stackoverflow.com/questions/52723904/every-other-element-in-an-array
            data = data["message"].flat() //removes nested part of list e.g [[1,2],[3,4]] = [1,2,3,4]
            if (timeframe == "1d"){ //the extra *2 comes from the timeframe being passed in the array
                data = data.slice(-24*2)
              }
              else if (timeframe == "1w"){
                data = data.slice(-24*7*2)
              }
              else if (timeframe == "1m"){
                data = data.slice(-24*7*30*2)
            }
            var chart = new Chart(document.getElementById("line-chart"), {
            type: 'line',
            data: {
                // Change below to label of data eg yearly
                labels: data.filter((_,i) => i&1),
                datasets: [{ 
                    // Change below to the data corresponding with the labels, eg yearlydata with yearly
                    data: data.filter((_,i) => i-1&1),
                    label: "PNL",
                    borderColor: "#f2a900",
                    fill: false
                }]
            },
            options: {
                scales:{
                    x: {
                        display: false
                    }
                },
                title: {
                display: true,
                }
            }
            });
            line_chart = chart
        }
    })
}

function change_to_percentages(data){
    var start = parseFloat(data[0])
    var percentages = [0]
    var sliced = data.slice(1)
    for (var i = 0; i < sliced.length; i++){
        percentages.push((parseFloat(sliced[i])-start)/parseFloat(sliced[i]))
    }
    return percentages
}

function get_historical(coin){
    var result = false
    $.ajax({
        url:`http://127.0.0.1:8000/api/portfolio/historical/?username=${coin}`,
        type:"GET",
        dataType:"json",
        success: function(data){
            //console.log(data["message"])
            eth_data = data["message"]
            callback(result)
        }
    })
    return result
}

function load_new_chart(coin){
    if (line_chart != false){ // if chart instance exists
        line_chart.destroy()
    }
    //var eth_data = get_historical("eth")
    //console.log(eth_data)
    //var btc_data = get_historical("eth")
    var eth_data = ['1119.1', '1124.5', '1123.4', '1125.1', '1124.9', '1125.0', '1123.9', '1122.9', '1124.1', '1122.7', '1124.7', '1127.5', '1128.4', '1130.6', '1134.9', '1138.5', '1141.2', '1141.8', '1149.8', '1150.6', '1151.4', '1149.6', '1147.3', '1149.0', '1147.6', '1149.7', '1149.5', '1156.1', '1152.0', '1149.5', '1149.2', '1152.1', '1150.4', '1151.5', '1152.4', '1153.2', '1154.6', '1153.8', '1156.9', '1166.8']
    //console.log(eth_perc)
    timeframe = global_timeframe
    console.log(timeframe)
    $.ajax({
        url:"http://127.0.0.1:8000/api/portfolio/historical/?username=0xd2b101d3a69b20ac140ce233a67dd88abb0222b1",
        type:"GET",
        dataType:"json",
        success: function(data){
            // ref https://stackoverflow.com/questions/52723904/every-other-element-in-an-array
            data = data["message"].flat() //removes nested part of list e.g [[1,2],[3,4]] = [1,2,3,4]
            var PNL =  data.filter((_,i) => i-1&1)
            if (timeframe == "1d"){ //the extra *2 comes from the timeframe being passed in the array
                data = data.slice(-24*2)
                eth_data = eth_data.slice(-24)
                PNL = PNL.slice(-24)
              }
              else if (timeframe == "1w"){
                data = data.slice(-24*7*2)
                eth_data = eth_data.slice(-24*7)
                PNL = PNL.slice(-24*7)
              }
              else if (timeframe == "1m"){
                data = data.slice(-24*7*30*2)
                eth_data = eth_data.slice(-24*7*30)
                PNL = PNL.slice(-24*30)
            }
            var PNL =  change_to_percentages(PNL)
            var eth_perc = change_to_percentages(eth_data)
            //console.log(change_to_percentages(data.filter((_,i) => i-1&1)))
            var _labels = data.filter((_,i) => i&1)
            var data = {
                labels: _labels,
                datasets: [{
                    label: "Portfolio",
                    data: PNL,
                    spanGaps: true,
                    borderColor: "#f2a900",
                  }, {
                    label: "Ethereum",
                    data: eth_perc,
                    spanGaps: false,
                    borderColor: "#37367b",
                  }
              
                ]
              };
            var options = {
                scales:{
                    x: {
                        display: false
                    }
                },
                title: {
                display: true,
                }
            }
            var chart = new Chart(document.getElementById("line-chart").getContext('2d'), {
                type: 'line',
                data: data,
                options: options
            })
            line_chart = chart
        }
    })
}

function load_pie_chart(){
    if (pie_chart != false){ // if chart instance exists
        pie_chart.destroy()
    }
    $.ajax({
        url:"http://127.0.0.1:8000/api/portfolio/balances",
        type:"GET",
        dataType:"json",
        success: function(data){
            data = data["message"]["portfolio"] //gets balances
            console.log(data)
            //console.log(data)
            var labels = []
            var prices = []
            for (var i in data){
                labels.push(data[i][0]) //gets label
                prices.push(data[i][2]) //gets value
            }var pchart = new Chart(document.getElementById("pie-chart"), {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{ 
                    data: prices,
                    label: "Pie Chart",
                    backgroundColor:["#00FFA3" , "#37367b", "#0004ff", "#FF0000", "#F00000", "#FFFF00", "#000000"],
                    fill: true
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
            }
            });
            pie_chart = pchart
        }
    })
}


$(document).ready(function() {
    load_chart()
    load_pie_chart()
    $("#1d").click(function(){
        load_chart("1d");
    }); 
    $("#1w").click(function(){
        load_chart("1w");
    }); 
    $("#1m").click(function(){
        load_chart("1m");
    }); 
    $("#All").click(function(){
        load_chart();
    }); 
    $("#ETH").click(function(){
        load_new_chart();
    }); 
});
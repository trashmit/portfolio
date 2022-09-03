function load_data(){
    $.ajax({
        url:"/api/portfolio/balances/",
        type:"GET",
        dataType:"json",
        success: function(data){
            var response = data["message"];
            var total = response["total"]
            console.log(total)
            console.log(typeof(total))
            if (total == 0){
                $("#balance").text("No balances! Add one in keys.");
                return;
            }
            var portfolio = response["portfolio"]
            console.log(portfolio)
            $("#balance").text(total);
            $("#coins > tbody").empty();
            for (var i = 0; i < portfolio.length; i++) {
                $('#coins').append(`
                <tr>
                    <td><img src="${portfolio[i][3]}" class="tokenimg me-3"><span class="tag1"></span>${portfolio[i][0]}</td>
                    <td><span class="tag2"></span> ${(parseFloat(portfolio[i][2]) / parseFloat(portfolio[i][1])).toFixed(2)}</td>
                    <td><span class="tag3"></span> ${parseFloat(portfolio[i][1]).toFixed(2)}</td> 
                    <td><span class="tag4"></span> ${parseFloat(portfolio[i][2]).toFixed(2)}</td>
                </tr>
                `)
            }
        }
    })
}

function auth_status(){
    $.ajax({
        url:"/api/users/check/",
        type:"GET",
        dataType:"json",
        success: function(data){
            if (data["status"] == "success"){
                $("#balance").text("Loading Balances.");
            }
            else{
                $("#balance").text(data["message"]);
            }   
        }
    })
}
window.onload = auth_status();
window.onload = load_data();

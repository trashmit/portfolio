function send_one_key() {
    var form_data = $('#blockchains').serializeArray()
    console.log(typeof(form_data[0]["value"]))
    $.ajax({
        url:`/api/keys/addkey/?network=${form_data[0]["value"]}&api_key=${form_data[1]["value"]}`,
        type:"POST",
        dataType:"json",
        success: function(data){
            $("#blockchain-text").text(data["message"])
        }
    })
  }

function send_two_key() {
    var form_data = $('#exchanges').serializeArray() //gets data from form!
    var keypair = `[${form_data[1]["value"]}, ${form_data[2]["value"]}]`
    console.log(keypair)
    $.ajax({
        url:`/api/keys/addkey/?network=${form_data[0]["value"]}&api_key=${keypair}`,
        type:"POST",
        dataType:"json",
        success: function(data){
            console.log(data)
            $("#exchange-text").text(data["message"])
        },
        error: function(data){
            console.log(data)
            $("#exchange-text").text("Invalid Api Keys")
        }
    })
}

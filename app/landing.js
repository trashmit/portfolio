sbtn = document.getElementById("sbtn");
lbtn = document.getElementById("lbtn");
lbtns = document.getElementById("LogIn");
sbtns = document.getElementById("SignUp");

lbtn.onclick = function(){
    lbtns.style.display = "none"
    sbtns.style.display = "block"
}

sbtn.onclick = function(){
    lbtns.style.display = "block"
    sbtns.style.display = "none"
}

$(document).ready(function(){
    $("#launch-modal").click(function(){
        if (typeof window.ethereum !== 'undefined') {
            $("#metamask-text").text("Connect to Metamask")
            //$("#metamask").click(eth_auth())
            //console.log("something")
        }
        else {
            $("#metamask-text").text("Install Metamask")
            //$("#metamask").click(redirect)
        }
    
        $("#login-modal").modal('show')
    });
})

function eth_auth(){
        console.log("WENT HERE")
        var address = ethereum.request({ method: 'eth_requestAccounts' }); 
        $.ajax({
            url:"/api/users/getnonce/?address=" + ethereum.selectedAddress,
            type:"GET",
            dataType:"json",
            success: function(data){
            const provider = new ethers.providers.Web3Provider(window.ethereum)
            const signer = provider.getSigner()
            var nonce = data["message"]
            var message = "verifying with: " + nonce
            //console.log(message)
            var signature = signer.signMessage("verifying with: " + nonce).then((signature) => {
            console.log(signature)
                $.ajax({
                    url:"/api/users/verifysignature/?address="+ethereum.selectedAddress+"&signature="+signature,
                    type:"POST",
                    dataType:"json",
                    success: function(data){
                        //console.log(data)
                        if(data["message"]=="fail"){    
                            $("#text").text("Login Failed")
                        }
                        else if(data["message"]=="success"){
                            //NEEDS FIXING
                            document.cookie= `access_token=${data["data"]["cookie"]}; expires=sat, 31 Dec 2022 00:00:00 UTC`
                            window.location.replace("/portfolio/");
                        }
                    }
            })
        });
    }
})}

function login(){
    var username = $('#logemail').val()
    var password = $('#logpass').val()
    $.ajax({
        url:`/api/users/signin/?username=${username}&password=${password}`,
        type:"POST",
        dataType:"json",
        success: function(data){
            console.log(data)
            if (data["message"] == "success") {
                //NEEDS FIXING
                document.cookie = `access_token=${data["data"]["cookie"]}; expires=sat, 31 Dec 2022 00:00:00 UTC`
                window.location.replace("/portfolio/");

            }
            else {
                $("#login_text").text("Username or password is incorrect, try again!")
            }
        }
    })
}

function password_strong(password){
    var upper = /[A-Z]/.test(password);
    var lower = /[a-z]/.test(password);
    var digit = /\d/.test(password);
    var symbol = /[-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]/.test(password);
    var L = password.length > 7;
    if (upper && lower && digit && symbol && L) {
        return true;
    }
    else {
        return false;
    }
}

function signup(){
    var username = $('#regemail').val()
    var password1 = $('#regpass').val()
    var password2 = $('#rregpass').val()
    if (username == "" || password1 =="" || password2=="") {
        $("#signup_text").text("Field is empty!")
        return 
    }

    if (password1 == password2) {
        if (password_strong(password1) == true) {
            $.ajax({
                url:`/api/users/signup/?username=${username}&password=${password1}`,
                type:"POST",
                dataType:"json",
                success: function(data){
                    console.log(data)
                    if (data["message"] == "success") {
                        $("#signup_text").text("Signup Successful")
                        document.cookie= `access_token=${data["data"]["cookie"]}; expires=sat, 31 Dec 2022 00:00:00 UTC`
                        window.location.replace("/portfolio/");
                    }
                    else {
                        $("#signup_text").text("Username is taken!")
                    }
                }
            })
        }
        else {
            $("#signup_text").text("Password is not strong enough!")
        }
    }
    else {
        $("#signup_text").text("Passwords do not match!")
    }
}

function sign_out (){
    alert("Sign out failed, try clearing cookies or restarting browser!")
}

function redirect(){
    window.open('https://metamask.io/')
}

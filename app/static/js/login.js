const base_url = "http://studentnet.cs.manchester.ac.uk/authenticate/?"
const return_url = "url=http://127.0.0.1:5000/pairingpage"
const csticket = Math.floor(Math.random() * 100)
const full_url = base_url + return_url + "&csticket=" + csticket + "&version=3&command=validate"


const login_button = document.getElementById("target")
login_button.addEventListener("click", goElsewhere)


function goElsewhere(){
    window.location.href = full_url
}
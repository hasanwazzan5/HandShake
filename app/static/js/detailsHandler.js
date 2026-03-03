document.addEventListener("DOMContentLoaded", () => {
    const details = new URLSearchParams(window.location.search)

    console.log(details.get("fullname"))
    console.log(details.get("username"))

    fetch('/login', {
        method: 'POST',
          headers: {
    'Content-Type': 'application/json'
                },
        body: JSON.stringify(
            {
                fullname: details.get("fullname"),
                username: details.get("username")
            }
        )
    })
    .then(result => console.log(result))
})
snap_btn = document.getElementById("snap");
video = document.querySelector("#video");
canvas = document.querySelector("#canvas");

// This one requests access to the camera, and displays the stream.
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) { 
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) { 
        video.srcObject = stream;
        video.play();
    })
}

snap_btn.addEventListener("click", async function() { 
    // This will take the image itself.
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    const imgData = canvas.toDataURL("image/png");
    const blob = await (await fetch(imgData)).blob();
    // Converts to binary, then converts to a blob, which can be sent to the server.

    const formData = new FormData();
    formData.append('file', blob, "image.png")

    var dataURL = canvas.toDataURL("image/png");
    fetch('/uploadtest', { 
        method: 'POST',
        body: formData
    })
    
})


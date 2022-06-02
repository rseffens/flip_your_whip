console.log("top line")

var carcreateform = document.getElementById('car-create')

carcreateform.addEventListener("submit", submitHandler)

function submitHandler(e){
    e.preventDefault()
    console.log(e.target)
    var carphoto = document.getElementById('car-photo')
    console.log(carphoto.files)
    var imageform = new FormData()
    imageform.append("image", carphoto.files[0])
    fetch("https://api.imgbb.com/1/upload?expiration=600&key=66651ee279d5770f8871457b92b3b597", {
        method: "POST",
        body: imageform
    })
        .then(response => response.json() )
        .then(coderData => {
            var form = new FormData(carcreateform)
            form.delete("photo")
            form.append("photo", coderData.data.url)
            fetch("/car/create", {
                method: "POST", 
                body: form
            })
            .then(response => response.json() )
            .then(data =>  {
                console.log(data)
                window.location.href = "/dashboard"
            })
            .catch(err => console.log(err) )
        } )
        console.log("success")
}

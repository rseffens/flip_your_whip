// console.log("hello")

var vinNum = document.querySelector("#vin-num")
console.log(vinNum);

vinNum.addEventListener('submit', function(event){
    event.preventDefault()
    let dispYear = document.getElementById('year')
    let dispMake = document.getElementById('make')
    let dispModel = document.getElementById('model')
    let dispTrim = document.getElementById('trim')
    let dispDoors = document.getElementById('doors')
    let dispSeats = document.getElementById('seats')
    let dispOrigin = document.getElementById('origin')
    let dispFuel = document.getElementById('fuel')
    let dispType = document.getElementById('type')

    let vin = this.children[0].value
    
    fetch(`https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/${vin}*BA?format=json`)
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
        let info = {
            year: data.Results[9].Value,
            make: data.Results[6].Value,
            model: data.Results[8].Value,
            trim: data.Results[11].Value,
            doors: data.Results[23].Value,
            seats: data.Results[46].Value,
            origin: data.Results[14].Value,
            fuel: data.Results[76].Value,
            type: data.Results[22].Value,
        };
        dispYear.innerText = info.year
        dispMake.innerText = info.make
        dispModel.innerText = info.model
        dispTrim.innerText = info.trim
        dispDoors.innerText = info.doors
        dispSeats.innerText = info.seats
        dispOrigin.innerText = info.origin
        dispFuel.innerText = info.fuel
        dispType.innerText = info.type
        
        console.log(info)
    })
    .catch(err => console.log(err))
})

const logout = async () => {
    console.log("logging out")
    const res = await fetch('http://127.0.0.1:5000/logout')
    console.log(res)
    if (res.error) {
        console.log("logout error")
    } else if (res.status == 200) {
        window.location.href = res.url
    }
}

const appointmentFormElement = document.getElementById("appointment-form")
const makeAppointmentBtn = document.getElementById("make-appointment-btn")

const getTimeSlots = (data) => {
    const times = [];
    const [startHour, startMinute] = data["starttime"].split(":").map(Number);
    const [endHour, endMinute] = data["endtime"].split(":").map(Number)

    for(let i=parseInt(startHour);i<parseInt(endHour);i++){
        times.push(`${i}:${endHour}-${i+1}:${endHour+1}`)
    }
    
    let slotHTML = ''
    times.forEach((item) => {
        slotHTML += `<button onclick="handleSlotBooking(event)" value="${item}-${data["doctorid"]}-${data["hospitalname"]}-${data['firstname']}-${data['lastname']}" id="selected-slot" class="ml-2 border border-black rounded-md">
            ${item}
        </button>`
    })
    
    return slotHTML;
}

const handleSlotBooking = (event) => {
    const data = event.target.value.split("-")
    document.getElementById("slot-confirm").innerHTML = `
        <div>
            <h1>Hospital : ${data[3]}</h1>
            <h1>Doctor Name : ${data[4]} ${data[5]}</h1>
            <h1>Time slot : ${data[0]} - ${data[1]}</h1>
            <button onclick="sendRequestForAppointment(event)" value="${data[0]}-${data[1]}-${data[2]}-${data[3]}-${data[4]}-${data[5]}">Submit</button>
        </div>
    `
}

const sendRequestForAppointment = async (event) => {
    const data = event.target.value.split("-")
    console.log(data)
    const response = await fetch("/submit/appointment", {
        method: "POST",
        body: JSON.stringify({
            doctorid: data[2],
            hospitalname: data[3],
            timeSlot: data[0]+"-"+data[1],
            doctorName: data[4]+" "+data[5]
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    const jsonResponse = await response.json()
    if (jsonResponse["status"] === "success") {
        console.log("success")
    }
}

document.getElementById("search-submit").addEventListener("click", async (event) => {
    const formData = new FormData(appointmentFormElement)
    const response = await fetch("/getsearchresults", {
        method: "POST",
        body: JSON.stringify(Object.fromEntries(formData.entries())),
        headers: {
            "Content-Type": 'application/json'
        }
    })
    const jsonResponse = await response.json()
    let searchHTML = ""
    jsonResponse.forEach((item) => {
        searchHTML += `<div>
            <p>${item.hospitalname} Hospital - ${item.firstname} Doctor</p>
        </div>
        <div>
            Available Slots - ${getTimeSlots(item)}
        </div>`
    })
    document.getElementById('search-results').innerHTML = searchHTML
})

appointmentFormElement.addEventListener("submit", (event) => {
    event.preventDefault()
    console.log("Submiting appointment")
    const formData = new FormData(appointmentFormElement);
    console.log(Object.fromEntries(formData.entries()))
})

document.getElementById("appointment-date").addEventListener("click", () => {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0');
    let yyyy = today.getFullYear()
    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("appointment-date").setAttribute("min", today);
})
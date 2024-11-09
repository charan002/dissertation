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

const appntbtn = document.getElementById("make-appointment-btn")
const Fdiv = document.getElementById("dialog")
const form = document.getElementById("appointment-form")
const wrongbtn = document.getElementById("wrong")
let appointmentContext = {}

appntbtn.addEventListener('click', function () {
    Fdiv.classList.remove("hidden")
    document.body.style.overflow = "hidden"
})
wrongbtn.addEventListener('click', () => {
    Fdiv.classList.add("hidden")
    document.body.style.overflow = ""
})

const appointmentFormElement = document.getElementById("appointment-form")
const makeAppointmentBtn = document.getElementById("make-appointment-btn")

const getTimeSlots = (data) => {
    const times = [];
    const [startHour, startMinute] = data["starttime"].split(":").map(Number);
    const [endHour, endMinute] = data["endtime"].split(":").map(Number)

    for (let i = parseInt(startHour); i < parseInt(endHour); i++) {
        times.push(`${i}:${endHour}-${i + 1}:${endHour + 1}`)
    }

    let slotHTML = ''
    times.forEach((item) => {
        slotHTML += `
        <option>
            ${item}
        </option>`
    })

    return slotHTML;
}

const handleSlotBooking = (timeslot) => {
    document.getElementById("slot-confirm").innerHTML = `
        <div>
            <h1 class="my-4">Please confirm your slot booking</h1>
            <div class="grid grid-cols-[40%_60%] items-center">
            <div class="text-right place-self-end mr-4">
                <svg class="text-right place-self-end" xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M480.29-496q24.04 0 40.88-17.12Q538-530.24 538-554.29q0-24.04-17.12-40.88Q503.76-612 479.71-612q-24.04 0-40.88 17.12Q422-577.76 422-553.71q0 24.04 17.12 40.88Q456.24-496 480.29-496ZM480-163.67q112-96 180.5-201.5T729-547q0-111.76-70.36-184.88Q588.28-805 480-805q-108.28 0-178.64 73.12Q231-658.76 231-547q0 76.33 68.83 181.83 68.84 105.5 180.17 201.5Zm0 32.67Q345-252 276-357t-69-190q0-120 78.5-200.5T480-828q116 0 194.5 80.5T753-547q0 85-69 190T480-131Zm0-423Z"/></svg>
            </div>
            <h1 class="text-left">${appointmentContext["hospitalname"]} Hospital</h1>
        </div>
        <div class="grid grid-cols-[40%_60%] items-center">
            <div class="text-right place-self-end mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M680-341q-35 0-59.5-24.5T596-425q0-35 24.5-59.5T680-509q35 0 59.5 24.5T764-425q0 35-24.5 59.5T680-341Zm0-24q25.33 0 42.67-17.33Q740-399.67 740-425q0-25.33-17.33-42.67Q705.33-485 680-485q-25.33 0-42.67 17.33Q620-450.33 620-425q0 25.33 17.33 42.67Q654.67-365 680-365ZM476-118v-80q0-11.57 5.53-21.75Q487.05-229.94 497-236q25.85-15.29 54.26-25.79Q579.68-272.29 609-278l71 95 70-95q29.81 5.71 58.27 16.21Q836.73-251.29 863-236q10 6 15 16t6 21v81H476Zm23-24h181.33l-81-108q-26.97 6.62-51.82 16.48-24.84 9.85-48.51 22.85V-142Zm181.33 0H860v-68.67q-23.67-13-48.85-22.33-25.18-9.33-51.48-16l-79.34 107Zm0 0Zm0 0Zm-451.85-30q-23.31 0-39.9-16.71Q172-205.42 172-228v-504q0-22.58 16.71-39.29T228-788h504q22.58 0 39.29 16.71T788-732v141.33q-5.67-4.33-11.5-7.83t-12.5-7.83V-732q0-14-9-23t-23-9H228q-14 0-23 9t-9 23v504q0 14 9 23t23 9h130.67q.66-.67 1-.67.33 0 .33-1.33v26H228.48ZM306-618h314q9-1.67 17.2-2.33 8.2-.67 16.8-2.67v-19H306v24Zm0 150h179q2-6.67 3.55-12.43 1.55-5.76 3.12-11.57H306v24Zm0 150h108q11.33-8.67 22.83-16.5 11.5-7.83 24.5-13.5v6H306v24ZM196-196v-568V-606.33-625-196Zm484-229Z"/></svg>
            </div>
            <h1 class="text-left">Dr. ${appointmentContext["firstname"]} ${appointmentContext["lastname"]} - ${appointmentContext["doctortype"]}</h1>
        </div>
        <div class="grid grid-cols-[40%_60%] items-center">
            <div class="text-right place-self-end mr-4">
                <svg class="text-right place-self-end" xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M228-132q-23.85 0-39.93-16.07Q172-164.15 172-188v-508q0-23.85 16.07-39.93Q204.15-752 228-752h85.33v-88H342v88h280v-88h25.33v88H732q23.85 0 39.93 16.07Q788-719.85 788-696v508q0 23.85-16.07 39.93Q755.85-132 732-132H228Zm0-24h504q12 0 22-10t10-22v-342H196v342q0 12 10 22t22 10Zm-32-398h568v-142q0-12-10-22t-22-10H228q-12 0-22 10t-10 22v142Zm0 0v-174 174Zm284 162q-11 0-19.5-8.5T452-420q0-11 8.5-19.5T480-448q11 0 19.5 8.5T508-420q0 11-8.5 19.5T480-392Zm-160 0q-11 0-19.5-8.5T292-420q0-11 8.5-19.5T320-448q11 0 19.5 8.5T348-420q0 11-8.5 19.5T320-392Zm320 0q-11 0-19.5-8.5T612-420q0-11 8.5-19.5T640-448q11 0 19.5 8.5T668-420q0 11-8.5 19.5T640-392ZM480-240q-11 0-19.5-8.5T452-268q0-11 8.5-19.5T480-296q11 0 19.5 8.5T508-268q0 11-8.5 19.5T480-240Zm-160 0q-11 0-19.5-8.5T292-268q0-11 8.5-19.5T320-296q11 0 19.5 8.5T348-268q0 11-8.5 19.5T320-240Zm320 0q-11 0-19.5-8.5T612-268q0-11 8.5-19.5T640-296q11 0 19.5 8.5T668-268q0 11-8.5 19.5T640-240Z"/></svg>
            </div>
            <h1 class="text-left">${appointmentContext["date"]} @ ${timeslot}</h1>
        </div>
        <button class="rounded-3xl mt-4" onclick="sendRequestForAppointment('${timeslot}')">Submit</button>
        </div>
    `
}

const sendRequestForAppointment = async (timeSlot) => {
    const response = await fetch("/submit/appointment", {
        method: "POST",
        body: JSON.stringify({
            doctorid: appointmentContext["doctorid"],
            hospitalname: appointmentContext["hospitalname"],
            timeSlot: timeSlot,
            doctorName: appointmentContext["firstname"] + " " + appointmentContext["lastname"],
            status: "TODO",
            date: appointmentContext["date"],
            doctortype: appointmentContext["doctortype"]
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    const jsonResponse = await response.json()
    if (jsonResponse["status"] === "success") {
        console.log("success")
        location.reload()
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
    let searchHTML = `
    <div class="grid grid-cols-[50%_50%] items-center mt-4">
        <div class="text-right place-self-end mr-4">
            <svg class="text-right place-self-end" xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M228-132q-23.85 0-39.93-16.07Q172-164.15 172-188v-508q0-23.85 16.07-39.93Q204.15-752 228-752h85.33v-88H342v88h280v-88h25.33v88H732q23.85 0 39.93 16.07Q788-719.85 788-696v508q0 23.85-16.07 39.93Q755.85-132 732-132H228Zm0-24h504q12 0 22-10t10-22v-342H196v342q0 12 10 22t22 10Zm-32-398h568v-142q0-12-10-22t-22-10H228q-12 0-22 10t-10 22v142Zm0 0v-174 174Zm284 162q-11 0-19.5-8.5T452-420q0-11 8.5-19.5T480-448q11 0 19.5 8.5T508-420q0 11-8.5 19.5T480-392Zm-160 0q-11 0-19.5-8.5T292-420q0-11 8.5-19.5T320-448q11 0 19.5 8.5T348-420q0 11-8.5 19.5T320-392Zm320 0q-11 0-19.5-8.5T612-420q0-11 8.5-19.5T640-448q11 0 19.5 8.5T668-420q0 11-8.5 19.5T640-392ZM480-240q-11 0-19.5-8.5T452-268q0-11 8.5-19.5T480-296q11 0 19.5 8.5T508-268q0 11-8.5 19.5T480-240Zm-160 0q-11 0-19.5-8.5T292-268q0-11 8.5-19.5T320-296q11 0 19.5 8.5T348-268q0 11-8.5 19.5T320-240Zm320 0q-11 0-19.5-8.5T612-268q0-11 8.5-19.5T640-296q11 0 19.5 8.5T668-268q0 11-8.5 19.5T640-240Z"/></svg>
        </div>
        <h1 class="text-left">${formData.get("date")}</h1>
    </div>`
    jsonResponse.forEach((item) => {
        appointmentContext = item
        searchHTML += `
        <div class="grid grid-cols-[50%_50%] items-center">
            <div class="text-right place-self-end mr-4">
                <svg class="text-right place-self-end" xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M480.29-496q24.04 0 40.88-17.12Q538-530.24 538-554.29q0-24.04-17.12-40.88Q503.76-612 479.71-612q-24.04 0-40.88 17.12Q422-577.76 422-553.71q0 24.04 17.12 40.88Q456.24-496 480.29-496ZM480-163.67q112-96 180.5-201.5T729-547q0-111.76-70.36-184.88Q588.28-805 480-805q-108.28 0-178.64 73.12Q231-658.76 231-547q0 76.33 68.83 181.83 68.84 105.5 180.17 201.5Zm0 32.67Q345-252 276-357t-69-190q0-120 78.5-200.5T480-828q116 0 194.5 80.5T753-547q0 85-69 190T480-131Zm0-423Z"/></svg>
            </div>
            <h1 class="text-left">${item.hospitalname} Hospital</h1>
        </div>
        <div class="grid grid-cols-[50%_50%] items-center">
            <div class="text-right place-self-end mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#434343"><path d="M680-341q-35 0-59.5-24.5T596-425q0-35 24.5-59.5T680-509q35 0 59.5 24.5T764-425q0 35-24.5 59.5T680-341Zm0-24q25.33 0 42.67-17.33Q740-399.67 740-425q0-25.33-17.33-42.67Q705.33-485 680-485q-25.33 0-42.67 17.33Q620-450.33 620-425q0 25.33 17.33 42.67Q654.67-365 680-365ZM476-118v-80q0-11.57 5.53-21.75Q487.05-229.94 497-236q25.85-15.29 54.26-25.79Q579.68-272.29 609-278l71 95 70-95q29.81 5.71 58.27 16.21Q836.73-251.29 863-236q10 6 15 16t6 21v81H476Zm23-24h181.33l-81-108q-26.97 6.62-51.82 16.48-24.84 9.85-48.51 22.85V-142Zm181.33 0H860v-68.67q-23.67-13-48.85-22.33-25.18-9.33-51.48-16l-79.34 107Zm0 0Zm0 0Zm-451.85-30q-23.31 0-39.9-16.71Q172-205.42 172-228v-504q0-22.58 16.71-39.29T228-788h504q22.58 0 39.29 16.71T788-732v141.33q-5.67-4.33-11.5-7.83t-12.5-7.83V-732q0-14-9-23t-23-9H228q-14 0-23 9t-9 23v504q0 14 9 23t23 9h130.67q.66-.67 1-.67.33 0 .33-1.33v26H228.48ZM306-618h314q9-1.67 17.2-2.33 8.2-.67 16.8-2.67v-19H306v24Zm0 150h179q2-6.67 3.55-12.43 1.55-5.76 3.12-11.57H306v24Zm0 150h108q11.33-8.67 22.83-16.5 11.5-7.83 24.5-13.5v6H306v24ZM196-196v-568V-606.33-625-196Zm484-229Z"/></svg>
            </div>
            <h1 class="text-left">Dr. ${item.firstname}</h1>
        </div>
        <div class="grid grid-cols-[50%_50%] items-center mb-8">
            <h1 class="my-2 text-right place-self-end mr-4">Available slots</h1>
            <form id="slot-booking-form" class="text-left">
                <select name="timeslot" class="border border-black rounded-3xl h-10 px-2">
                    ${getTimeSlots(item)}
                </select>
            </form>
        </div>
        <button class="rounded-3xl mb-4" onclick="handleSlotSelection(event)">Book Slot</button>`
    })
    form.classList.add("hidden")
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

const handleSlotSelection = (event) => {
    event.preventDefault()
    document.getElementById("search-results").classList.toggle("hidden")
    console.log(appointmentContext)
    const formData = new FormData(document.getElementById("slot-booking-form"))
    console.log(formData.get("timeslot"))
    handleSlotBooking(formData.get("timeslot"))
}
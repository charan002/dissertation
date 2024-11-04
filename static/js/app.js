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

makeAppointmentBtn.addEventListener("click", () => {
    
})

appointmentFormElement.addEventListener("submit", (event) => {
    event.preventDefault()
    console.log("Submiting appointment")
    const formData = new FormData(appointmentFormElement);
    console.log(Object.fromEntries(formData.entries()))
})
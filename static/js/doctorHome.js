document.getElementById("date-report").addEventListener("click", () => {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0');
    let yyyy = today.getFullYear()
    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("date-report").setAttribute("min", today);
})

document.getElementById('time-report-submit-btn').addEventListener("click", async (event) => {
    event.preventDefault()
    const formData = new FormData(document.getElementById("time-report-form"))
    const response = await fetch("/doc/submit/timereport", {
        method: "POST",
        body: JSON.stringify(Object.fromEntries(formData.entries())),
        headers: {
            "Content-Type": "application/json"
        }
    })
    console.log(response)
})

const doctorLogout = async () => {
    console.log("logging out")
    const res = await fetch('http://127.0.0.1:5000/doc/logout')
    console.log(res)
    if (res.error) {
        console.log("logout error")
    } else if (res.status == 200) {
        window.location.href = res.url
    }
}

const handleStatusChange = async (event) => {
    event.preventDefault()
    const submitChange = await fetch("/doc/appointment/changestatus", {
        method: "POST",
        body: JSON.stringify({
            id: event.target.value,
            statusChange: "INPROGRESS"
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const response = await submitChange.json()
    if (response['status'] === "success") {
        location.reload()
    }
}

const handleAppointmentClick = (username, id) => {
    window.location.href = `/doc/patientdetails?username=${username}&id=${id}`
}
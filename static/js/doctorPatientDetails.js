const handleStatusChange = async (event) => {
    event.preventDefault()
    const urlParams = new URLSearchParams(window.location.search)
    const submitChange = await fetch("/doc/appointment/changestatus", {
        method: "POST",
        body: JSON.stringify({
            id: urlParams.get('id'),
            statusChange: event.target.value
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

const updatePrescriptionAndRemarks = async (event) => {
    const remarks = document.getElementById("remarks-content").value
    const prescription = document.getElementById("prescription-content").value
    console.log(event.target.getAttribute("data-mydata"))
    const id = JSON.parse(event.target.getAttribute("data-mydata"))["_id"]
    const response = await fetch("/doc/submit/prescriptionAndRemarks", {
        method: "POST",
        body: JSON.stringify({
            id: id,
            prescription: prescription,
            remarks: remarks
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    const jsonResponse = await response.json()
    if (jsonResponse["status"] == "success") {
        document.getElementById(`update-success-message`).classList.remove("hidden")
        document.getElementById(`update-failure-message`).classList.add("hidden")
    } else {
        document.getElementById("update-failure-message").classList.remove("hidden")
        document.getElementById("update-success-message").classList.add("hidden")
    }
}

const insertEnabledPrescriptionIfStatusInProgress = (data) => {
    if (data['status'] == "INPROGRESS") {
        document.getElementById("apptmt-prescription").innerHTML = `
            
            <label class="self-center text-2xl">Prescribe below</label>
            <br>
            <textarea class="border h-24 border-black rounded-3xl p-4" id="prescription-content"
                draggable="false" style="resize: none;">${data["prescription"] ? data["prescription"] : ""}</textarea>
        `
    } else if (data['status'] == "DONE") {
        document.getElementById("apptmt-prescription").innerHTML = ` 
            
            <label class=" self-center text-2xl">Prescription</label>
            <br>
            <textarea class="border h-24 border-black rounded-3xl p-4" id="prescription-content"
                draggable="false" style="resize: none;" disabled>${data["prescription"] ? data["prescription"] : ""}</textarea>
        `
    } else if (data['status'] == "TODO") {
        document.getElementById("apptmt-prescription").innerHTML = ``
    }
}

const insertButtonElement = (data) => {
    if (data["status"] == "INPROGRESS") {
        document.getElementById("prescription-div").innerHTML = `
            <button data-mydata='${JSON.stringify(data)}' onclick="updatePrescriptionAndRemarks(event)" id="prescription-submit-btn" class="border rounded-3xl">Submit</button>
        `
    } else {
        document.getElementById("prescription-div").innerHTML = ``
    }
}

const insertStatusElement = (data) => {
    console.log(data)
    if (data['status'] != "DONE") {
        document.getElementById("apptmt-status-change").innerHTML = `
        <label class="place-self-end self-center mr-4">Change Status</label>
        <select id="status-dropdown" class="border border-black rounded-3xl h-10 px-4"
            onchange="handleStatusChange(event)">
            <option disabled selected>Select</option>
            <option value="TODO">Todo</option>
            <option value="INPROGRESS">Inprogress</option>
            <option value="DONE">Done</option>
        </select>`
        document.getElementById("apptmt-status").innerHTML = `${data["status"]}`
    } else {
        document.getElementById("apptmt-status").innerHTML = `${data["status"]}`
        document.getElementById("apptmt-status-change").innerHTML = ``
    }
}

const insertRemarksElement = (data) => {
    if (data['status'] == "INPROGRESS") {
        document.getElementById("apptmt-remarks").innerHTML = `
            <label class="self-center text-2xl">Enter Remarks</label>
            <br>
            <textarea class="border h-24 border-black rounded-3xl p-4" id="remarks-content"
                draggable="false" style="resize: none;">${data["remarks"] ? data["remarks"] : ""}</textarea>
        `
    } else if (data['status'] == "DONE") {
        document.getElementById("apptmt-remarks").innerHTML = `
            <label class="self-center text-2xl">Remarks</label>
            <br>
            <textarea class="border h-24 border-black rounded-3xl p-4" id="remrks-content-disabled"F
                draggable="false" style="resize: none;" disabled>${data["remarks"] ? data["remarks"] : ""}</textarea>
        `
    } else if (data['status'] == "TODO") {
        document.getElementById("apptmt-remarks").innerHTML = ``
    }
}

const handleAppointmentChange = (event) => {
    console.log(event.currentTarget)
    let data = JSON.parse(event.currentTarget.getAttribute("data-mydata"))
    console.log(data)
    document.getElementById("apptmt-doctorid").innerHTML = data['doctorid']
    document.getElementById("apptmt-date").innerHTML = data['date']
    document.getElementById("apptmt-timeslot").innerHTML = data['timeSlot']
    insertStatusElement(data)
    insertRemarksElement(data)
    insertEnabledPrescriptionIfStatusInProgress(data)
    insertButtonElement(data)
}
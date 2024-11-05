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

const updatePrescription = async () => {
    const data = document.getElementById("prescription-content").value
    console.log(data)
    const urlParams = new URLSearchParams(window.location.search)
    const response = await fetch("/doc/submit/prescription", {
        method: "POST",
        body: JSON.stringify({
            id: urlParams.get("id"),
            prescription: data
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
}
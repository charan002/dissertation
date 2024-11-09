const logout = async () => {
    console.log("logging out")
    const res = await fetch('http://127.0.0.1:5000/pharma/logout')
    console.log(res)
    if (res.error) {
        console.log("logout error")
    } else if (res.status == 200) {
        window.location.href = res.url
    }
}


const handleUserPrescription = async (event) => {
    event.preventDefault();
    const phoneNumberForm = document.getElementById("phone-number-form")
    const formData = new FormData(phoneNumberForm);
    const response = await fetch("/pharma/getPrescriptions", {
        method: "POST",
        body: JSON.stringify({
            phoneNumber: formData.get("phonenumber")
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const jsObj = await response.json()
    console.log(jsObj)
    prescriptionHTML = ""
    jsObj.forEach(ele => {
        prescriptionHTML += `
            <div>
                ${ele['prescription']}
            </div>
        `
    })
    document.getElementById("user-prescriptions").innerHTML = prescriptionHTML
}

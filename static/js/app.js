async function logout() {
    console.log("got here")
    const res = await fetch('http://127.0.0.1:5000/logout')
    console.log(res)
    if (res.error) {
        console.log("logout error")
    } else if (res.status == 200) {
        window.location.href = res.url
    }
} 
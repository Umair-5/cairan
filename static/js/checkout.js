function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.querySelector("#checkout").addEventListener('click',(event)=>{
    event.preventDefault();
    const customerName=document.querySelector("#customer_name").value;
    const customerNumber=document.querySelector("#phone_num").value;
    const customerEmail=document.querySelector("#email").value;
    const customerAddress=document.querySelector("#address").value;
    const customerCity=document.querySelector("#city").value;
    const customerState=document.querySelector("#state").value;
    const customerCountry=document.querySelector("#country").value;
    if (!customerName || !phoneNumber || !email || !address || !city) {
        alert('Please fill in all required fields.');
        return;
    }
    fetch('/place_order/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            customer_name:customerName,
            customer_number:customerNumber,
            customer_email:customerEmail,
            customer_address:customerAddress,
            customer_city:customerCity,
            customer_state:customerState,
            customer_country:customerCountry

        })
    })
    .then(response=> response.json())
    .then(data=>{
        if (data.success===true){
            console.log("Order Placed")
            window.location.href='/'
        }
    })
    .catch(error=>console.error(error));
});
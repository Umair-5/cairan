let changeMainImage = (newSrc) => {
    document.getElementById('display-image').src = newSrc;
}

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

const sizeButtons = document.querySelectorAll('.size-btn');
let selectedSize = ''; 

sizeButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault(); 
        selectedSize = button.value;
        sizeButtons.forEach(btn => btn.style.backgroundColor = "");
        button.style.backgroundColor = "#C9C9C9";
        document.getElementById('selected-size').value = selectedSize;
    });
});

const form = document.querySelector('#add-to-cart-form'); 

if (form) {
    form.addEventListener('submit', (e) => {
        e.preventDefault(); 

        if (!selectedSize) {
            alert('Please select a size!'); 
            return;
        }

        fetch('/add_to_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() 
            },
            body: new URLSearchParams({
                product_id: form.querySelector('input[name="product_id"]').value,
                size: selectedSize 
            }).toString() 
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            showAddedToCartPopup();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}


document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.getAttribute('data-id');

        fetch(`/delete/${productId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to delete item.');

            const itemContainer = this.closest('.cart-container');
            itemContainer.remove();

            const remainingItems = document.querySelectorAll('.cart-container').length;
            if (remainingItems === 0) {
                document.getElementById('empty-cart').style.display = 'flex';
                document.getElementById('cart-info').style.display = 'none';
            }

            const itemPriceText = this.closest('.cart-item-text').querySelector('.item_price').innerText;
            const itemPrice = parseFloat(itemPriceText.replace('RS. ', '').trim());

            const totalPriceElement = document.getElementById('total-price');
            let currentTotalPrice = parseFloat(totalPriceElement.innerText.replace('Total Price: RS. ', '').trim());

            const newTotalPrice = currentTotalPrice - itemPrice;
            totalPriceElement.innerText = `Total Price: RS. ${newTotalPrice.toFixed(2)}`;
        })
        .catch(error => console.error('Error:', error));
    });
});



function showAddedToCartPopup() {
    const popup = document.querySelector('.added-to-cart');
    popup.style.opacity = '1';
    popup.style.visibility = 'visible';
    document.querySelector('.close-btn').addEventListener('click', hideAddedToCartPopup);

}

function hideAddedToCartPopup() {
    const popup = document.querySelector('.added-to-cart');
    popup.style.opacity = '0';
    popup.style.visibility = 'hidden';
}

document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function () {
        const action = this.dataset.action;
        const productId = this.dataset.id;
        const size = this.closest('.cart-item-text').querySelector('.item-size').innerText.replace('Size: ', '').trim(); 
        fetch('/update_quantity/', {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                product_id: productId,
                size: size,
                action: action
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 'success') {
                const quantityElement = this.closest('.cart-item-text').querySelector('#item-quantity');
                quantityElement.innerHTML = `<span>Quantity: </span>${data.quantity}`;
                const price= document.querySelector("#total-price");
                price.innerText=`Total Price: RS. ${data.total_price}`
            } else if (data.status === 'failed') {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});


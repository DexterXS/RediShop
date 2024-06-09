console.log("JavaScript is running!");

document.addEventListener('DOMContentLoaded', function() {
    const productGrid = document.querySelector('.product-grid');

    if (productGrid) {
        const products = [
            { id: 1, name: 'Product 1', price: 10 },
            { id: 2, name: 'Product 2', price: 15 },
            { id: 3, name: 'Product 3', price: 20 },
            { id: 4, name: 'Product 4', price: 25 },
            { id: 5, name: 'Product 5', price: 30 },
            { id: 6, name: 'Product 6', price: 35 },
            { id: 7, name: 'Product 7', price: 40 },
            { id: 8, name: 'Product 8', price: 45 },
            { id: 9, name: 'Product 9', price: 50 },
            { id: 10, name: 'Product 10', price: 55 },
            { id: 11, name: 'Product 11', price: 60 },
            { id: 12, name: 'Product 12', price: 65 },
            { id: 13, name: 'Product 13', price: 70 },
            { id: 14, name: 'Product 14', price: 75 },
            { id: 15, name: 'Product 15', price: 80 },
            { id: 16, name: 'Product 16', price: 85 }
        ];

        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.classList.add('product');
            productDiv.innerHTML = `
                <h3>${product.name}</h3>
                <p>Price: $${product.price}</p>
                <button onclick="addToCart(${product.id})">Add to Cart</button>
            `;
            productGrid.appendChild(productDiv);
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams(data)
                });
                if (response.ok) {
                    console.log("Login successful, redirecting to profile...");
                    window.location.href = '/profile';
                } else {
                    const errorData = await response.json();
                    document.getElementById('errorMessage').innerText = errorData.detail || JSON.stringify(errorData);
                }
            } catch (error) {
                document.getElementById('errorMessage').innerText = "Error submitting data. Please try again.";
            }
        });
    }
});

function addToCart(productId) {
    alert(`Product ${productId} added to cart`);
}

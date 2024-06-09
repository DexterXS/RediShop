document.getElementById('addProductForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const response = await fetch('/add_product', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        alert('Product added successfully!');
        e.target.reset();
        // Обновите список продуктов
    } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
    }
});

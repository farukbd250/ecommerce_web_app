document.querySelectorAll('.btn-minus, .btn-plus, .btn-danger').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.dataset.itemId;
        const action = this.classList.contains('btn-plus') ? 'increase' : 
                        this.classList.contains('btn-minus') ? 'decrease' : 'remove';

        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: action }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Refresh the page to show updated cart
            }
        });
    });
});

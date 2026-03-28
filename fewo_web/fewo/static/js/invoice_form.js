document.addEventListener('DOMContentLoaded', function () {
    const propertySelect = document.getElementById('id_rental_property');
    const priceInput = document.getElementById('id_price_per_night');
    const breakfastPriceInput = document.getElementById('id_breakfast_price');
    const taxPercentInput = document.getElementById('id_tax_percent');
    const includeBreakfastCheckbox = document.getElementById('id_include_breakfast');

    function toggleBreakfastPrice() {
        if (breakfastPriceInput && includeBreakfastCheckbox) {
            const group = breakfastPriceInput.closest('.form-group');
            if (group) {
                group.style.display = includeBreakfastCheckbox.checked ? 'block' : 'none';
            }
        }
    }

    if (includeBreakfastCheckbox) {
        includeBreakfastCheckbox.addEventListener('change', toggleBreakfastPrice);
        toggleBreakfastPrice();
    }

    function loadPropertyDetails(propertyId) {
        if (!propertyId) return;

        fetch(`/properties/${propertyId}/details/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (priceInput && !priceInput.value) priceInput.value = data.price_per_night;
                if (breakfastPriceInput && !breakfastPriceInput.value) breakfastPriceInput.value = data.default_breakfast_price;
                if (taxPercentInput && !taxPercentInput.value) taxPercentInput.value = data.default_tax_percent;
            })
            .catch(error => console.error('Error fetching property details:', error));
    }

    if (propertySelect) {
        propertySelect.addEventListener('change', function () {
            const propertyId = this.value;
            if (propertyId) {
                fetch(`/properties/${propertyId}/details/`)
                    .then(response => response.json())
                    .then(data => {
                        if (priceInput) priceInput.value = data.price_per_night;
                        if (breakfastPriceInput) breakfastPriceInput.value = data.default_breakfast_price;
                        if (taxPercentInput) taxPercentInput.value = data.default_tax_percent;
                    })
                    .catch(error => console.error('Error fetching property details:', error));
            }
        });

        if (propertySelect.value) {
            if (priceInput && !priceInput.value) {
                loadPropertyDetails(propertySelect.value);
            }
        }
    }
});

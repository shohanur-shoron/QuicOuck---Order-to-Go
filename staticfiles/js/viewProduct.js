const quantityInput = document.getElementById('quantityInput')
const plusButton = document.getElementById('quantityplus')
const minusButton = document.getElementById('quantityminus')
const currentPrice = document.getElementById('currentPrice')
const totalPrice = document.getElementById('totalPrice')

plusButton.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value) || 1;
    quantity++;
    quantityInput.value = quantity;
    const currentPriceText = currentPrice.textContent;
    const currentPriceint = parseFloat(currentPriceText);
    totalPrice.textContent = currentPriceint * quantity;
});

minusButton.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value) || 1;
    if (quantity > 1) {
        quantity--;
    }
    quantityInput.value = quantity;
    const currentPriceText = currentPrice.textContent;
    const currentPriceint = parseFloat(currentPriceText);
    totalPrice.textContent = currentPriceint * quantity;
});

quantityInput.addEventListener('change', () => {
    const currentPriceText = currentPrice.textContent;
    const currentPriceint = parseFloat(currentPriceText);
    totalPrice.textContent = currentPriceint * quantityInput.value;
});


const timeDisplay = document.getElementById('pickup_time_display');
const pickupTimeInput = document.getElementById('pickup_time');


function formatDatetime(dateTimeString) {
    const dateTime = new Date(dateTimeString);
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    };
    const formattedTime = dateTime.toLocaleString('en-US', options);
    const [date, time] = formattedTime.split(', ');
    return `Date: ${date.split('/').reverse().join('/')} and Time: ${time}`;
}

timeDisplay.value = 'Now';

timeDisplay.addEventListener('click', () => {
    pickupTimeInput.showPicker();
});

pickupTimeInput.addEventListener('change', () => {
    timeDisplay.value = formatDatetime(pickupTimeInput.value);
});
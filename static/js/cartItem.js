const moneyInCartItem1 = document.querySelectorAll('#moneyInCartItem1')
const totalMoneyInCartItem = document.querySelectorAll('#totalMoneyInCartItem')
const quantityInput1 = document.querySelectorAll('#cartQuantityDiv')
const totalMoney = document.getElementById('totalCartMoney')

let totalMoneyInCart = 0;

for(let i = 0; i<moneyInCartItem1.length; i++) {
    const moneyInCartItemText = moneyInCartItem1[i].textContent;
    const moneyInCartItemInt = parseInt(moneyInCartItemText);
    totalMoneyInCartItem[i].textContent = moneyInCartItemInt * parseInt(quantityInput1[i].textContent);
    totalMoneyInCart += parseInt(totalMoneyInCartItem[i].textContent);
    totalMoney.textContent = totalMoneyInCart;
}


const timeDisplay2 = document.querySelectorAll('#pickup_time_display_cart');
const pickupTimeInput2 = document.querySelectorAll('#pickup_time_cart');


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

for(let i = 0; i<timeDisplay2.length; i++){
    timeDisplay2[i].value = 'Now';
}


for(let i = 0; i<timeDisplay2.length; i++){
    timeDisplay2[i].addEventListener('click', () => {
        pickupTimeInput2[i].showPicker();
    });
}

for(let i = 0; i<timeDisplay2.length; i++){
    pickupTimeInput2[i].addEventListener('change', () => {
        timeDisplay2[i].value = formatDatetime(pickupTimeInput2[i].value);
    });
}

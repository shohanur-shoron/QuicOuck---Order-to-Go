const QuantityInCustomarPage = document.querySelectorAll('#QuantityInCustomarPage');
const unitPriceInCustomerPage = document.querySelectorAll('#unitPriceInCustomerPage');
const totalPriceInCustomarPage = document.querySelectorAll('#totalPriceInCustomarPage');

for(let i=0; i<QuantityInCustomarPage.length; i++){
    totalPriceInCustomarPage[i].textContent = unitPriceInCustomerPage[i].textContent * QuantityInCustomarPage[i].textContent;
}
VANTA.NET({
    el: "#container",
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00,
    color: 0xffffff,
    backgroundColor: 0x95afc0,
    points: 13.00,
    showDots: false
})

var inputField7 = document.getElementById("phoneNumberlogin");
var inputField8 = document.getElementById("passwordlogin");


inputField7.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Phone Number');
});

inputField8.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Password');
});

inputField7.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField8.addEventListener("input", function(event) {
    this.setCustomValidity('');
});
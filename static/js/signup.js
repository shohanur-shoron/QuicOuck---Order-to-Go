
const selectImage = document.querySelector('.selectImage');
const inputFile = document.querySelector('#imageUpload');
const imgArea = document.querySelector('.img-area');

selectImage.addEventListener('click', function () {
	inputFile.click();
})

inputFile.addEventListener('change', function () {
	const image = this.files[0]
	const reader = new FileReader();
    reader.onload = ()=> {
        const allImg = imgArea.querySelectorAll('img');
        allImg.forEach(item=> item.remove());
        const imgUrl = reader.result;
        const img = document.createElement('img');
        img.src = imgUrl;
        imgArea.appendChild(img);
        imgArea.classList.add('active');
        imgArea.dataset.img = image.name;
    }
    reader.readAsDataURL(image);
})



const inputView = document.getElementById('inputView');

function moveRight(){
    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const phoneNumberInput = document.getElementById("phoneNumber");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmPassword");


    
    if (firstNameInput.value !== "" && lastNameInput.value !== "" && phoneNumberInput.value !== "" && emailInput.value !== "" && passwordInput.value !== "" && confirmPasswordInput.value !== "") {
        

        if(passwordInput.value !== confirmPasswordInput.value){
            passwordInput.classList.add('chackPassWrong')
            confirmPasswordInput.classList.add('chackPassWrong')
            alert ("Password did not match!!!");
        }
        else{
            passwordInput.classList.remove('chackPassWrong')
            confirmPasswordInput.classList.remove('chackPassWrong')
            passwordInput.classList.add('chackPassOk')
            confirmPasswordInput.classList.add('chackPassOk')
            inputView.classList.add('moveRight')
        }
    }
    else{
        alert ("Please Fill-Up the Form");

        if(firstNameInput.value === ""){
            firstNameInput.classList.add('chackPassWrong')
        }
        if(lastNameInput.value === ""){
            lastNameInput.classList.add('chackPassWrong')
        }
        if(phoneNumberInput.value === ""){
            phoneNumberInput.classList.add('chackPassWrong')
        }
        if(emailInput.value === ""){
            emailInput.classList.add('chackPassWrong')
        }

        if(passwordInput.value === ""){
            passwordInput.classList.add('chackPassWrong')
        }
        if(confirmPasswordInput.value === ""){
            confirmPasswordInput.classList.add('chackPassWrong')
        }

        //next

        if(firstNameInput.value !== ""){
            firstNameInput.classList.remove('chackPassWrong')
        }
        if(lastNameInput.value !== ""){
            lastNameInput.classList.remove('chackPassWrong')
        }
        if(phoneNumberInput.value !== ""){
            phoneNumberInput.classList.remove('chackPassWrong')
        }
        if(emailInput.value !== ""){
            emailInput.classList.remove('chackPassWrong')
        }

        if(passwordInput.value !== ""){
            passwordInput.classList.remove('chackPassWrong')
        }
        if(confirmPasswordInput.value !== ""){
            confirmPasswordInput.classList.remove('chackPassWrong')
        }
        
    }

    
}

function moveBack(){
    inputView.classList.remove('moveRight')
}

var inputField1 = document.getElementById("firstName");
var inputField2 = document.getElementById("lastName");
var inputField3 = document.getElementById("phoneNumber");
var inputField4 = document.getElementById("email");
var inputField5 = document.getElementById("password");
var inputField6 = document.getElementById("confirmPassword");
    

inputField1.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter First Name');
});

inputField2.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Last Name');
});

inputField3.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Phone Number');
});

inputField4.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Email Address');
});

inputField5.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Enter Password');
});

inputField6.addEventListener("invalid", function(event) {
    this.setCustomValidity('Please Reenter Your Password');
});

// Clear custom validity when input is considered valid
inputField1.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField2.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField3.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField4.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField5.addEventListener("input", function(event) {
    this.setCustomValidity('');
});

inputField6.addEventListener("input", function(event) {
    this.setCustomValidity('');
});
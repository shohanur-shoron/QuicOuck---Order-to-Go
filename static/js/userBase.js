const navBar = document.getElementById('navBar')
const infoRightBtm = document.getElementById('infoRightBtm')
const searchBox = document.getElementById('searchBox')
const cartItems1 = document.getElementById('cartItems1')
let lastScroll = 0;

window.addEventListener("scroll", function () {
    const currentScroll = window.scrollY;

    if(currentScroll === 0){
        infoRightBtm.classList.add('opacity1')
        infoRightBtm.classList.remove('opacity0')
        cartItems1.classList.remove('opacity1')
        cartItems1.classList.add('opacity0')
        infoRightBtm.style.zIndex = '10'
        navBar.classList.remove('transformHalf')
        navBar.classList.remove('transformFull')
        searchBox.classList.remove('showSearch')
        searchBox.style.pointerEvents = 'none'
    }

    if(currentScroll > lastScroll){
        navBar.classList.add('transformFull')
    }

    if(currentScroll <= lastScroll && currentScroll!==0){
        navBar.classList.add('transformHalf')
        navBar.classList.remove('transformFull')
        searchBox.classList.add('showSearch')
        infoRightBtm.classList.remove('opacity1')
        infoRightBtm.classList.add('opacity0')
        infoRightBtm.style.zIndex = '-1'
        cartItems1.classList.add('opacity1')
        cartItems1.classList.remove('opacity0')
        searchBox.style.pointerEvents = 'all'
    }

    lastScroll = currentScroll;
})

const profileInfo = document.getElementById('profileInfo')
function closeProfile(){
    profileInfo.style.transform = 'translateX(101%)'
}

function openProfile(){
    profileInfo.style.transform = 'translateX(0%)'
}

const searchBox1 = document.getElementById('searchBoxTextInput1')
const searchBox2 = document.getElementById('searchBoxTextInput2')

searchBox1.addEventListener('input', function (){
    searchBox2.value = this.value
});

searchBox2.addEventListener('input', function (){
    searchBox1.value = this.value
});
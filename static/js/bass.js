const navBar = document.getElementById('navBar')
const infoRightBtm = document.getElementById('infoRightBtm')
const searchBox = document.getElementById('searchBox')
let lastScroll = 0;

window.addEventListener("scroll", function () {
    const currentScroll = window.scrollY;

    if(currentScroll === 0){
        infoRightBtm.classList.remove('zindex3')
        navBar.classList.remove('transformHalf')
        navBar.classList.remove('transformFull')
        searchBox.classList.remove('showSearch')
    }

    if(currentScroll > lastScroll){
        navBar.classList.add('transformFull')
    }

    if(currentScroll <= lastScroll && currentScroll!==0){
        navBar.classList.add('transformHalf')
        navBar.classList.remove('transformFull')
        searchBox.classList.add('showSearch')
        infoRightBtm.classList.add('zindex3')
    }

    lastScroll = currentScroll;
})
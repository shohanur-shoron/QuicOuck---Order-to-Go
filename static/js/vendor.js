const navbar = document.getElementById('navbar')
let lastScroll = 0;

window.addEventListener('scroll', (e)=>{
    const currentScroll = window.scrollY;

    if(currentScroll > lastScroll){
        navbar.classList.add('navbarTransform')
    }

    if(currentScroll <= lastScroll){
        navbar.classList.remove('navbarTransform')
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
const imageForCard = document.querySelectorAll('#imageForCard')
const topLayer = document.querySelectorAll('#topLayer')

let firstTime = true

if(firstTime){
    for(let i=0; i<topLayer.length; i++){
        topLayer[i].classList.add('removeLayer')
    }
    firstTime = false
}

for(let i = 0; i<imageForCard.length; i++) {
    imageForCard[i].addEventListener('mouseenter', function(e){
        topLayer[i].classList.remove('removeLayer')
    });

    imageForCard[i].addEventListener('mouseleave', function(e){
        topLayer[i].classList.add('removeLayer')
    });
}


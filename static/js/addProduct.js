const selectImage = document.querySelector('.selectImage');
const inputFile = document.querySelector('#imageUpload');
const imgArea = document.querySelector('.img-area');
const defaultImageUrl = inputFile.src;

selectImage.addEventListener('click', function () {
	inputFile.click();
})

const defaultImg = document.createElement('img');
defaultImg.src = defaultImageUrl;
imgArea.appendChild(defaultImg);


inputFile.addEventListener('change', function () {
	const image = this.files[0]
	if(true) {
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
	}
})
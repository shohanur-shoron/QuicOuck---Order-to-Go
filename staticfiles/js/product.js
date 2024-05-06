let valueDisplays = document.querySelectorAll(".numAni");
let targetDuration = 1000;
let startTime;

valueDisplays.forEach((valueDisplay) => {
    let startValue = 0;
    let endValue = parseInt(valueDisplay.getAttribute("data-val"));

    let step = Math.ceil((targetDuration / (endValue - startValue) * 10) / 10);

    let animationFrame = (timestamp) => {
        if (startTime === undefined) startTime = timestamp;
        let progress = Math.min((timestamp - startTime) / targetDuration, 1);
        let currentValue = Math.floor(startValue + progress * (endValue - startValue));

        valueDisplay.textContent = currentValue;

        if (currentValue < endValue) {
            requestAnimationFrame(animationFrame);
        } else {
            valueDisplay.textContent = endValue;
        }
    };

    requestAnimationFrame(animationFrame);
});

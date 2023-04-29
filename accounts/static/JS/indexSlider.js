var images = ["accounts\static\images\slide1.png","accounts\static\images\slide2.png"]

var i=0;
document.body.style.backgroundImage = `url('${images[i]}')`

setInterval(() => {
    i = (i+1)%images.length;
    document.body.style.backgroundImage = `url('${images[i]}')`
}, 5000);
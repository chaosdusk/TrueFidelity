var canvases = document.getElementsByTagName('canvas');

for (var i = 0; i < canvases.length; i++) {
    setupCanvas(canvases[i])
}

function setupCanvas(canvas) {
    var ctx = canvas.getContext("2d");
    var width = canvas.width;
    var height = canvas.height;
    var curX, curY, prevX, prevY;
    var hold = false;
    ctx.lineWidth = 2;

    var input = document.getElementById("length")

    canvas.onmousedown = function (e){
        var BB = canvas.getBoundingClientRect();

        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - BB.left;
        prevY = e.clientY - BB.top
        hold = true;
    };

    canvas.onmousemove = function linemove(e){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (hold){
            var BB = canvas.getBoundingClientRect();
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - BB.left;
            curY = e.clientY - BB.top;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            // canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();
            input.value = Math.sqrt((curX - prevX) ** 2 + (curY - prevY) ** 2).toFixed(0);
        }
    };

    canvas.onmouseup = function (e){
            hold = false;
    };

    canvas.onmouseout = function (e){
            hold = false;
    };
}

// Select an image
var imageA = document.getElementById("imageA");
var imageB = document.getElementById("imageB");

imageA.addEventListener("mousedown", function() {
    console.log("clicked A");
    var ww = Math.floor(Math.random() * 100);
    var wl = Math.floor(Math.random() * 100);
    console.log(ww)
    console.log(wl)
    document.getElementById("imageAimage").src = "imagedata/" + wl + "/" + ww + "/false.png";
    imageA.nextElementSibling.classList.add("selected");
    imageB.nextElementSibling.classList.remove("selected");

});


imageB.addEventListener("mousedown", function() {
    console.log("clicked B");
    imageB.nextElementSibling.classList.add("selected");
    imageA.nextElementSibling.classList.remove("selected");
});


// Range change values
function helloWorld(val, image) {
    console.log(val);
    document.getElementById(image).src = "imagedata/" + val + "/" + val + "/false.png";
}

function updateWW(ww, image) {
    console.log(ww);
    const prevSrc = document.getElementById(image).src;
    console.log("Previous src", prevSrc);
    const match = prevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/(.*)/)
    console.log(match)
    document.getElementById(image).src = "imagedata/" + match[1] + "/" + ww + "/" + match[3];
}

function updateWL(wl, image) {
    console.log(wl);
    const prevSrc = document.getElementById(image).src;
    console.log("Previous src", prevSrc);
    const match = prevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/(.*)/)
    console.log(match)
    document.getElementById(image).src = "imagedata/" + wl + "/" + match[2] + "/" + match[3];
}
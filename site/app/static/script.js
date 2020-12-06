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
    ctx.strokeStyle = "#FF0000";

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
            input.value = (Math.sqrt((curX - prevX) ** 2 + (curY - prevY) ** 2) / width * 100).toFixed(0);
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
    imageA.nextElementSibling.classList.add("selected");
    imageB.nextElementSibling.classList.remove("selected");
    document.getElementById('sideChosen-' + imageA.getAttribute('value')).checked = true;
});


imageB.addEventListener("mousedown", function() {
    console.log("clicked B");
    imageB.nextElementSibling.classList.add("selected");
    imageA.nextElementSibling.classList.remove("selected");
    document.getElementById('sideChosen-' + imageB.getAttribute('value')).checked = true;
});

document.getElementById('sideChosen').addEventListener("change", function() {
    // Should we select imageA? (ie: is imageA's position equal to the checked position?)
    if ((imageA.getAttribute('value') == 0) == document.getElementById('sideChosen-0').checked) {
        imageA.nextElementSibling.classList.add("selected");
        imageB.nextElementSibling.classList.remove("selected");
    } else {
        imageB.nextElementSibling.classList.add("selected");
        imageA.nextElementSibling.classList.remove("selected");
    }
})

// Range change values
function helloWorld(val) {
    console.log(val);
}


// Deprecated versions since only need one
function updateWW(ww, image) {
    console.log(ww);
    const prevSrc = document.getElementById(image).src;
    console.log("Previous src", prevSrc);
    const match = prevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    console.log(match)
    document.getElementById(image).src = "/imagedata/" + match[1] + "/" + match[2] + "/" + ww + "/" + match[4];
}

function updateWL(wl, image) {
    console.log(wl);
    const prevSrc = document.getElementById(image).src;
    console.log("Previous src", prevSrc);
    const match = prevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    console.log(match)
    document.getElementById(image).src = "/imagedata/" + match[1] + "/" + wl + "/" + match[3] + "/" + match[4];
}


const imageAimage = document.getElementById('imageAimage')
const imageBimage = document.getElementById('imageBimage')
function updateWW(ww) {
    const AprevSrc = imageAimage.src;
    const Amatch = AprevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    imageAimage.src = "/imagedata/" + Amatch[1] + "/" + Amatch[2] + "/" + ww + "/" + Amatch[4];

    const BprevSrc = imageBimage.src;
    const Bmatch = BprevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    imageBimage.src = "/imagedata/" + Bmatch[1] + "/" + Bmatch[2] + "/" + ww + "/" + Bmatch[4];
}

function updateWL(wl) {
    const AprevSrc = imageAimage.src;
    const Amatch = AprevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    imageAimage.src = "/imagedata/" + Amatch[1] + "/" + wl + "/" + Amatch[3] + "/" + Amatch[4];

    const BprevSrc = imageBimage.src;
    const Bmatch = BprevSrc.match(/imagedata\/([0-9]+)\/([0-9]+)\/([0-9]+)\/(.*)/)
    imageBimage.src = "/imagedata/" + Bmatch[1] + "/" + wl + "/" + Bmatch[3] + "/" + Bmatch[4];
}

// Scroll to the current image
const scrollbarCurrent = document.getElementById('current-index');
const parentDivPosition = scrollbarCurrent.parentElement.parentElement.offsetTop;
const currentDivPosition = scrollbarCurrent.offsetTop
document.getElementById('sidebar-links').scrollTop = currentDivPosition - parentDivPosition - 35;
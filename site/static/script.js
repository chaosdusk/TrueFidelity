var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
ctx.lineWidth = 2;
var fill_value = true;
var stroke_value = false;
var canvas_data = {"pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": []}

var input = document.getElementById("fname")

// line tool

function line(){

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
            console.log("hi");
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - BB.left;
            curY = e.clientY - BB.top;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            // canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();
            input.value = Math.sqrt((curX - prevX) ** 2 + (curY - prevY) ** 2).toFixed(2);
        }
    };

    canvas.onmouseup = function (e){
         hold = false;
    };

    canvas.onmouseout = function (e){
         hold = false;
    };
}

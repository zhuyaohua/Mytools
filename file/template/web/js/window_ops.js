
console.log("before window.onload")
window.onload = function () {
    console.log("inside window.onload")
    document.onkeydown = function (e) {
        data.type = 48;
        data.extraType = 0;
        data.dx = 0;
        data.dy = 0;
        data.posx = 0;
        data.posy = 0;
        //'a' keycode
        if (e.keyCode == 65) {
            data.posx = -0.1;
            ws1.send(code(data));
        }
        //'s' keycode
        if (e.keyCode == 83) {
            data.posy = -0.1;
            ws1.send(code(data));
        }
        //'d' keycode
        if (e.keyCode == 68) {
            data.posx = 0.1;
            ws1.send(code(data));
        }
        //'w' keycode
        if (e.keyCode == 87) {
            data.posy = 0.1;
            ws1.send(code(data));
        }
        //'q' keycode
        if (e.keyCode == 81) {
            data.dx = -1;
            ws1.send(code(data));
        }
        //'e' keycode
        if (e.keyCode == 69) {
            data.dx = 1;
            ws1.send(code(data));
        }
        //'z' keycode
        if (e.keyCode == 90) {
            data.dy = -1;
            ws1.send(code(data));
        }
        //'x' keycode
        if (e.keyCode == 88) {
            data.dy = 1;
            ws1.send(code(data));
        }
        //'m' keycode
        if (e.keyCode == 77) {
            data.extraType = 1;
            ws1.send(code(data));
        }
        //'n' keycode
        if (e.keyCode == 78) {
            data.extraType = 2;
            ws1.send(code(data));
        }
        if (e.keyCode == 16)
            shiftkey = true;
        if (e.keyCode == 17)
            ctrlkey = true;
        if (e.keyCode == 32) {
            data.extraType = 5;
            ws1.send(code(data));
        }
    }
    document.onkeyup = function (e) {
        if (e.keyCode == 16)
            shiftkey = false;
        if (e.keyCode == 17)
            ctrlkey = false;
    }
}

console.log("after window.onload")
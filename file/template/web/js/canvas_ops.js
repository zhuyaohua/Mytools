
showcanvas.onmouseup = function (e) {
    isUp = true;
    isDown = false;
    if (cullbox) {
        data.type = cullboxMouseDown + 2;
        data.posx = e.x;
        data.posy = e.y;
        ws1.send(code(data));
    }

    if (doFrameSelection) {
        data.type = 76;
        data.dx = x;
        data.dy = y;
        data.posx = e.x;
        data.posy = e.y;
        if (ctrlkey)
            data.extraType = 2;
        if (shiftkey)
            data.extraType = 4;
        ws1.send(code(data));
    }

    showcanvas.removeEventListener('mousemove', send);
    showcanvas.addEventListener('mousemove', normal_send);
}
showcanvas.onwheel = function (e) {

    data.dx = 0;
    data.dy = 0;
    data.posx = e.x;
    data.posy = e.y;

    if (e.wheelDelta > 0) {
        data.type = 10
    } else {
        data.type = 20
    }
    data.extraType = 0;
    {
        
        ws1.send(code(data))
        isrecv = false;
    }
}

showcanvas.onmousedown = function (e) {
    x = e.x
    y = e.y
    isDown = true;
    isUp = false;
    if (cullbox) {
        data.type = cullboxMouseDown;
        data.posx = e.x;
        data.posy = e.y;
        ws1.send(code(data));
    }
    showcanvas.addEventListener('mousemove', send);
    showcanvas.removeEventListener('mousemove', normal_send);

}
showcanvas.onclick = function (e) {
    if(multAreaSelect){
        data.type = 1021;
        posx = e.x.toString();
        posy = e.x.toString();
        data.uuid = '1;0;2;' + posx + ';' + posy;
        ws1.send(code(data));
        isrecv = false;
        isClickCanvas = true;
    }else if (!doFrameSelection) {
        data.type = 40;
        if (data.flag) {
            data.type = 28;
        }
        data.extraType = batchselect;
        data.dx = 0;
        data.dy = 0;
        data.posx = e.x;
        data.posy = e.y;
        data.uuid = 'd60623da-34b4-4a87-94b3-001f36ba96e1-0006db38'

        if(measuring)
            data.extraType = 1;
        if (ctrlkey)
            data.extraType = 2;
        if (shiftkey)
            data.extraType = 4;
	if (marking)
	    data.extraType = 3;
        
        if(attractive)
            data.dx = 1;

        ws1.send(code(data));
        isrecv = false;
        isClickCanvas = true;
    }
}

showcanvas.ondblclick = function (e) {
    data.type = 1007;
    data.dx = 0;
    data.dy = 0;
    data.posx = e.x;
    data.posy = e.y;
    ws1.send(code(data));
}

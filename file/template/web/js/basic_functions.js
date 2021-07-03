// function definitions
function fun_stringToByte_bak(str) {
    var bytes = new Array();
    var len, c;
    len = str.length;
    for (var i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if (c >= 0x010000 && c <= 0x10FFFF) {
            bytes.push(((c >> 18) & 0x07) | 0xF0);
            bytes.push(((c >> 12) & 0x3F) | 0x80);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        }
        else if (c >= 0x000800 && c <= 0x00FFFF) {
            bytes.push(((c >> 12) & 0x0F) | 0xE0);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        }
        else if (c >= 0x000080 && c <= 0x0007FF) {
            bytes.push(((c >> 6) & 0x1F) | 0xC0);
            bytes.push((c & 0x3F) | 0x80);
        }
        else {
            bytes.push(c & 0xFF);
        }
    }
    return bytes;
}

function fun_code_bak(data) {
    var strArray = fun_stringToByte_bak(data.uuid);
    var buffer = new ArrayBuffer(48 + strArray.length)
    var dv = new DataView(buffer)

    dv.setUint32(0, data.type);
    dv.setUint32(4, data.extraType);
    dv.setUint32(8, data.dx);
    dv.setUint32(12, data.dy);
    dv.setFloat32(16, data.posx);
    dv.setFloat32(20, data.posy);
    dv.setFloat32(24, data.anx);
    dv.setFloat32(28, data.asx);
    dv.setFloat32(32, data.any);
    dv.setFloat32(36, data.asy);
    dv.setFloat32(40, data.anz);
    dv.setFloat32(44, data.asy);
    var count = strArray.length;
    for (var item = 0; item < count; item++) {
        dv.setUint8(48 + item, strArray[item]);

    }

    return buffer
}

function send(e) {

    if (doFrameSelection) {
        ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight, 0, 0, 1280, 720);
        ctx.strokeStyle = "red";
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y);
        ctx.lineTo(x, e.y);
        ctx.lineTo(e.x, e.y);
        ctx.lineTo(e.x, y);
        ctx.lineTo(x, y);
        ctx.stroke();
    } else if (cullbox && !isUp && isDown) {
        data.type = cullboxMouseDown + 1;
        data.posx = e.x;
        data.posy = e.y;
        data.dx = e.x - x;
        data.dy = e.y - y;
        x = e.x;
        y = e.y;
        ws1.send(code(data));
        return;
    } else {
        var dx = e.x - x;
        var dy = e.y - y;

        data.posx = e.x;
        data.posy = e.y;

        if (e.buttons == 1) {

            data.type = 50;
            data.extraType = 0;
        }
        else if (e.buttons == 4) {
            if (dy < 0)
                data.type = 10;
            else
                data.type = 20;
        }
        else {
            data.type = 100;
        }
        data.dx = dx;
        data.dy = dy;
        console.log("x", x)
        console.log("y", y)

        if (dx == 0 && dy == 0) return;
        if (Math.abs(dx) < 2 && Math.abs(dy) < 2) return;
        if (isDown) {
            ws1.send(code(data));
            isrecv = false;
            x = e.x
            y = e.y
        }
    }
}

function normal_send(e) {
    if(catchNearPoint)
    {
        data.type = 91;
        data.extraType = 0;
        data.posx = e.x;
        data.posy = e.y;
        data.dx = catchNearPointType;
        data.dy = 0;
        ws1.send(code(data));
    }
}

function stringToByte(str) {
    var bytes = new Array();
    var len, c;
    len = str.length;
    for (var i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if (c >= 0x010000 && c <= 0x10FFFF) {
            bytes.push(((c >> 18) & 0x07) | 0xF0);
            bytes.push(((c >> 12) & 0x3F) | 0x80);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        }
        else if (c >= 0x000800 && c <= 0x00FFFF) {
            bytes.push(((c >> 12) & 0x0F) | 0xE0);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        }
        else if (c >= 0x000080 && c <= 0x0007FF) {
            bytes.push(((c >> 6) & 0x1F) | 0xC0);
            bytes.push((c & 0x3F) | 0x80);
        }
        else {
            bytes.push(c & 0xFF);
        }
    }
    return bytes;
}

function code(data) {
    console.log("==============================================");
    console.log("send:type:",data.type,"extraType:",data.extraType,",dx:",data.dx,",dy:",data.dy,",posx:",data.posx,",posy:",data.posy,",uuid:",data.uuid);
    var strArray = stringToByte(data.uuid);
    var buffer = new ArrayBuffer(48 + strArray.length)
    var dv = new DataView(buffer)

    dv.setUint32(0, data.type);
    dv.setUint32(4, data.extraType);
    dv.setUint32(8, data.dx);
    dv.setUint32(12, data.dy);
    dv.setFloat32(16, data.posx);
    dv.setFloat32(20, data.posy);
    dv.setFloat32(24, data.anx);
    dv.setFloat32(28, data.asx);
    dv.setFloat32(32, data.any);
    dv.setFloat32(36, data.asy);
    dv.setFloat32(40, data.anz);
    dv.setFloat32(44, data.asz);
    var count = strArray.length;
    for (var item = 0; item < count; item++) {
        dv.setUint8(48 + item, strArray[item]);

    }

    return buffer
}
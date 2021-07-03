function onDrawPointCallBack() {
    console.log("onDrawPointCallBack()")
    console.log("x: ", posx, " y: ", posy)
    drawPoint(posx, posy);
}

function drawPoint(x, y) {
    // let can = document.getElementById("modelView");
    let can = document.getElementById("showcanvas");
    let ctx = can.getContext("2d");
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#40E0D0";
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = "#40E0D0";
    ctx.stroke();
    ctx.closePath();
}
document.getElementById("checkAllResultsNoDisplay").onclick = function(e) {
    console.log("checkAllResultsNoDisplay")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;

    data.dx = 0;
    data.dy = 0;
    data.uuid = '0;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;32;99'; {
        // data.uuid = '0;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;5;20'; {

        ws1.send(code(data));
        isrecv = false;
        x = e.x
        y = e.y
    }
};
document.getElementById("showAllHeights").onclick = function(e) {
    console.log("showAllHeights")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = '1;0;0';

    {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("highlightSingleHeight").onclick = function(e) {
    console.log("highlightSingleHeight")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "2;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;A-6#;30";

    {
        ws1.send(code(data));
        isrecv = false;
    }
};


document.getElementById("showAllGreenLine").onclick = function(e) {
    console.log("showAllGreenLine")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "3;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;A-6#;30";

    {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("showSingleGreenLine").onclick = function(e) {
    console.log("showSingleGreenLine")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "4;1;2;44ccc9d4-eb7e-44f4-ab00-6a857b63b9e4_0;A-6#;30";

    {
        ws1.send(code(data));
        isrecv = false;
    }
};

document.getElementById("showAllBlueLine").onclick = function(e) {
    console.log("showAllBlueLine")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "7;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;A-6#;30";

    {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("showSingleBlueLine").onclick = function(e) {
    console.log("showSingleBlueLine")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "8;1;2;89decf94-d338-453c-92d1-97a05bbe4bc3-0012d10f;A-6#;30";

    {
        ws1.send(code(data));
        isrecv = false;
    }
};


//道路红线
document.getElementById("showRoadLine").onclick = function(e) {
    console.log("showRoadLine")
    data.posx = 0;
    data.posy = 0;

    data.type = 1006;
    data.dx = 0;
    data.dy = 0;
    data.uuid = "5;0;0";
    console.log(data.uuid); 
    {
        ws1.send(code(data));
        isrecv = false;
    }
};
//用地检测线
document.getElementById("showLandLine").onclick = function(e) {
    console.log("showLandLine")
    data.type = 1006;
    data.uuid = "11;0;0";
    console.log(data.uuid); 
    {
        ws1.send(code(data));
        isrecv = false;
    }
};
//用电力黑线
document.getElementById("showElectricBlackLine").onclick = function(e) {
    console.log("showElectricBlackLine")
    data.type = 1006;
    data.uuid = "11;0;0";
    console.log(data.uuid); 
    {
        ws1.send(code(data));
        isrecv = false;
    }
};
//地铁橙线
document.getElementById("SubwayOrangeLine").onclick = function(e) {
    console.log("SubwayOrangeLine")
    data.type = 1006;
    data.uuid = "15;0;0";
    console.log(data.uuid); 
    {
        ws1.send(code(data));
        isrecv = false;
    }
};
//蓝线
document.getElementById("showBlueLine").onclick = function(e) {
    console.log("showBlueLine")
    data.type = 1006;
    data.uuid = "7;0;0";
    console.log(data.uuid); 
    {
        ws1.send(code(data));
        isrecv = false;
    }
};



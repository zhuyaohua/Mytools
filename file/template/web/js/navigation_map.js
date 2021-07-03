function onMessageEmbedding() {

}



function showNavmap() {
    data_bak.type = 103;
    data_bak.uuid = "SendPositionInfo";
    ws1_bak.send(fun_code_bak(data_bak));
    document.getElementById("Navmap").style.display = "block";
}

function hideNavmap() {
    data_bak.type = 103;
    data_bak.uuid = "CloseSendPositionInfo";
    ws1_bak.send(fun_code_bak(data_bak));
    document.getElementById("Navmap").style.display = "none";
}



function arrayBuffer2String(buffer) {
    var dv = new DataView(buffer);
    var uuid = [];
    for (i = 0; i < buffer.byteLength; i++) {

        uuid.push(String.fromCharCode(dv.getInt8(i)));
    }
    return uuids = uuid.join("");

}

//sz_data:{
//    "message": "navigationWindow:147,368;-0.687766,-0.725933",
//    "type": "OutputNavPos"
//}
function reDrawNavigationPoint(uuid)
{
    if (uuid.indexOf("navigationWindow:") == 0) {
        uuid = uuid.split(":")[1];
        var pos = uuid.split(";");
        var x = pos[0].split(",")[0];
        var y = pos[0].split(",")[1];
        var dirX = pos[1].split(",")[0];
        var dirY = pos[1].split(",")[1];
        //console.log("navi win:"+x+","+y+","+dirX+","+dirY);
        document.getElementById("navigationCircle").setAttribute("cx", x);
        document.getElementById("navigationCircle").setAttribute("cy", y);
        var trianglePos = getTriangle(x, y, dirX, dirY);
        document.getElementById("navigationpolygon").setAttribute("points", trianglePos);
    }
}

function getTriangle(px, py, pdirX, pdirY) {
    var x = parseFloat(px)
    var y = parseFloat(py)
    var dirX = parseFloat(pdirX)
    var dirY = parseFloat(pdirY)
    var pos1X = x + dirX * 17;
    var pos1Y = y + dirY * 17;
    var tempx = x + dirX * 6;
    var tempy = y + dirY * 6;
    var vdir = rotateDirect(Math.PI / 2, dirX, dirY);
    var vdirX = parseFloat(vdir.split(",")[0]);
    var vdirY = parseFloat(vdir.split(",")[1]);
    var pos2X = tempx + vdirX * 6;
    var pos2Y = tempy + vdirY * 6;
    vdirX = -vdirX;
    vdirY = -vdirY;
    var pos3X = tempx + vdirX * 6;
    var pos3Y = tempy + vdirY * 6;
    return pos1X + "," + pos1Y + " " + pos2X + "," + pos2Y + " " + pos3X + "," + pos3Y;
}

function rotateDirect(angle, px, py) {
    var x = parseFloat(px)
    var y = parseFloat(py)
    cosVal = Math.cos(angle);
    sinVal = Math.sin(angle);
    var vx = x * cosVal - y * sinVal;
    var vy = x * sinVal + y * cosVal;
    return vx + "," + vy;
}

function isNavMapImage(){
    if ("navigationChart"== reuuid)
	{
		//console.log("navigationChart");
        return true;
	}
	//console.log("not navigationChart");
    return false;
}
var nav_imgUrl;
var nav_img = new Image();
function drawNavMapImage(blob, start){
	console.log(start,"drawNavMapImage");
    nav_imgUrl = URL.createObjectURL(blob.slice(start));
    nav_img.src = nav_imgUrl;
    nav_img.onload = function() {
		console.log("Navmap");
		var nav_canvas = document.getElementById('navmap');
        var nav_ctx = nav_canvas.getContext('2d');
        nav_ctx.drawImage(nav_img, 0, 0, this.naturalWidth, this.naturalHeight, 0, 0, 480, 480);
		
        document.getElementById("Navmap").style.backgroundImage = 'url("' + nav_canvas.toDataURL() + '")';
        document.getElementById("Navmap").style.backgroundRepeat = "no-repeat";
        document.getElementById("Navmap").style.backgroundPosition = "center";
        document.getElementById("Navmap").style.backgroundSize = "cover";
        window.URL.revokeObjectURL(nav_img);
    };
}
document.getElementById("nav_SetBuildNumber").onclick = function(e) {
    console.log("nav_SetBuildNumber");
    var bn = document.getElementById("nav_BuildNumber").value;
    data.type = 103;
    data.uuid = "SetBuildNumber:"+bn; 
    console.log(data.uuid);
    ws1.send(code(data));
    doNavMapScreenShot();
}
document.getElementById("nav_SetFloorHeight").onclick = function(e) {
    console.log("nav_SetFloorHeight");
    var fh = document.getElementById("nav_FloorHeight").value;
    data.type = 103;
    data.uuid = "SetFloorHeight:" +fh;
    ws1.send(code(data));
    doNavMapScreenShot();
}
document.getElementById("Navmap").onclick = function(e) {
    console.log("Navmap");
    var odiv=document.getElementById('Navmap');
    var x = odiv.getBoundingClientRect().left;
    var y = odiv.getBoundingClientRect().top;
    data.type = 103;
    data.dx = e.x-x;
    data.dy = e.y-y;
    data_bak.uuid = "PicPosToCameraPos";
    ws1.send(code(data));
}


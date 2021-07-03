document.getElementById("measure16").onclick = function(e) {
    console.log("measure16")
    data.type = 91;
    data.extraType = 16;
    ws1.send(code(data));
    measuring = true;
    document.getElementById("attractive_mode").removeAttribute("disabled");
}
document.getElementById("measure5").onclick = function(e) {
    console.log("measure5")
    data.type = 91;
    data.extraType = 5;
    ws1.send(code(data));
    measuring = false;
    document.getElementById("attractive_mode").setAttribute("disabled", true);
}

document.getElementById("attractive_mode").onclick = function(e) {
    console.log("attractive_mode")
    attractive = !attractive;
    if(attractive)
    {
        this.innerHTML ="吸附:打开";
    }else{
        this.innerHTML ="吸附:关闭";
    }
}

document.getElementById("deleteMeasure").onclick = function(e) {
    console.log("deleteMeasure")
    data.type = 91;
    data.extraType = 17;
    data.dx = 0;
    ws1.send(code(data));
}

document.getElementById("cleanMeasure").onclick = function(e) {
    console.log("cleanMeasure")
    data.type = 91;
    data.extraType = 18;
    data.dx = 0;
    ws1.send(code(data));
}

document.getElementById("restartMeasure").onclick = function(e) {
    console.log("restartMeasure")
    data.type = 91;
    data.extraType = 18;
    data.dx = 1;
    ws1.send(code(data));
}
document.getElementById("backOnePoint").onclick = function(e) {
    console.log("backOnePoint")
    data.type = 91;
    data.extraType = 18;
    data.dx = 2;
    ws1.send(code(data));
}
document.getElementById("closeEnd").onclick = function(e) {
    console.log("closeEnd")
    data.type = 91;
    data.extraType = 18;
    data.dx = 3;
    ws1.send(code(data));
}
document.getElementById("openEnd").onclick = function(e) {
    console.log("openEnd")
    data.type = 91;
    data.extraType = 18;
    data.dx = 4;
    ws1.send(code(data));
}
document.getElementById("multAreaSelectStart").onclick = function(e) {
    multAreaSelect = true;
}
document.getElementById("multAreaSelectEnd").onclick = function(e) {
    multAreaSelect = false;
}
document.getElementById("multAreaCollect").onclick = function(e) {
    data.type = 1021;
    data.uuid = '3;0;0';
    ws1.send(code(data));
}

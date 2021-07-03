document.getElementById("drawArea").onclick = function(e) {
    console.log("drawArea")
    data.type = 1028;
    data.uuid = '2;1;16;1234;1;0;0;0.5;5;5;5;5;-5;5;5;-5;-5;5;5;-5';
    ws1.send(code(data));
    data.type = 1028;
    data.uuid = '2;1;16;1236;0;1;0;0.5;5;5;5;-5;5;5;-5;5;-5;5;5;-5';
    ws1.send(code(data));
    data.type = 1028;
    data.uuid = '2;1;16;1235;0;0;1;0.5;5;5;5;-5;5;5;-5;-5;5;5;-5;5';
    ws1.send(code(data));
}
document.getElementById("cleanAllArea").onclick = function(e) {
    console.log("cleanAllArea")
    data.type = 1028;
    data.uuid = '0;0;0';
    ws1.send(code(data));
}

document.getElementById("delAreaByUuid").onclick = function(e) {
    console.log("delAreaByUuid")
    console.log("cleanAllArea")
    data.type = 1028;
    data.uuid = '1;1;0;1234';
    ws1.send(code(data));
   
}


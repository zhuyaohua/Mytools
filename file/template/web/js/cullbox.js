document.getElementById("resetCullBox").onclick = function(e) {

    data.type = 83;
    ws1.send(code(data));
};
document.getElementById("resetCullBox_debug").onclick = function(e) {

    data.extraType = 0;
    data.type = 1004;
    // extraType;uuid num;param num;min x;min y;min z;max x;max y;max z;direction
    data.uuid = "0;0;7;0.806;-2.9;-2.51;122.738;18.95;11;0";
    ws1.send(code(data));
};
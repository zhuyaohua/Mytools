// document.getElementById("batSwitch").onclick = function(e) {
//     batchselect = 2 - batchselect;
//     var batchBtn = document.getElementById("batSwitch");
//     if (batchselect == 2)
//         batchBtn.innerText = "批量选择开";
//     else
//         batchBtn.innerText = "批量选择关";
// }
console.log("before area_plane")
document.getElementById("area_plane_cancel").onclick = function(e) {
    data.type = 106;
    data.extraType = 0; {

        ws1.send(code(data));
        isrecv = false;
    }
    console.log("area_plane_cancel")
};
document.getElementById("area_plane").onclick = function(e) {
    console.log("area_plane")
    data.type = 106;
    data.extraType = 1;
    data.uuid = "3051aaaf-b848-4ad4-abc6-918802ac05fe-001315f9;3051aaaf-b848-4ad4-abc6-918802ac05fe-001315fc;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac"; {

        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("highlight_plane_color").onclick = function(e) {
    data.type = 1001;
    // extraType; uuid number; parameter number =6; uuid0; uuid1; ...;red0;green0;blue0;red1;green1;blue1
    {
        ws1.send(code(data));
        isrecv = false;
    }
    console.log("area_plane")
};
console.log("before building_cull")
document.getElementById("building_cull").onclick = function(e) {
    console.log("building_cull")
    data.type = 1005;
    // extraType;uuid num;param num;bldg_id;[low_limit];[high_limit];direction
    // data.uuid = "2;1;3;BLDG_ID;0.1;10.1;0";
    // data.uuid = "1;1;2;BLDG_ID;10.1;0";
    // data.uuid = "0;1;1;BLDG_ID;0";
    data.uuid = "1;1;2;7#;10.1;0"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("model_highlight").onclick = function(e) {
    console.log("model_highlight")
    data.type = 1000;
    data.uuid = "0;1;8;5364a2d1-819c-4904-9282-c47fda358241-000bd0cf;1;0;0;1;0;1;0;1"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("model_persist_highlight").onclick = function(e) {
    console.log("model_persist_highlight")
    data.type = 1099;
    // data.uuid = "1;1;10;27d491ba-cfe6-48a9-8a28-51b6079e44a3-000516e9;0;1;1;0;0;1;0.1;1;0;1";
    data.uuid = "1;1;10;27d491ba-cfe6-48a9-8a28-51b6079e44a3-000516e9;0;1;1;0;0;1;0.1;1;1;0"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("model_persist_highlight_reset").onclick = function(e) {
    console.log("model_persist_highlight_reset")
    data.type = 1099;
    data.uuid = "0;0;0"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
console.log("before cam level")
document.getElementById("set_cam_level").onclick = function(e) {
    console.log("set_cam_level")
    data.type = 103;
    data.uuid = "SetCameraLevel";
    data.dx = 0; {
        ws1.send(code(data));
        isrecv = false;
    }
};
console.log("before render cull box")
document.getElementById("renderCullBox").onclick = function(e) {
    data.type = 46;
    cullbox = !cullbox;
    data.extraType = cullbox ? 1 : 0;
    if (cullbox) {
        document.getElementById("renderCullBox").innerText = "隐藏剖切盒";
    } else {
        document.getElementById("renderCullBox").innerText = "显示剖切盒";
    }
    ws1.send(code(data));
}
console.log("after render cull box")
document.getElementById("area_highlight").onclick = function(e) {
    data.type = 1001;
    // extraType; uuid number; parameter number =6; uuid0; uuid1; ...;red0;green0;blue0;red1;green1;blue1
    data.uuid = "1;1;6;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;1;0;0;0;0;1"; {
        ws1.send(code(data));
        isrecv = false;
    }
    console.log("area_plane")
};
document.getElementById("building_highlight").onclick = function(e) {
    console.log("building_highlight")
    data.type = 1003;
    // extraType;uuid num;param num;bldg_id;[low_limit];[high_limit];direction
    data.uuid = "1;1;3;7#;1;0;0"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
document.getElementById("mixed_highlight").onclick = function(e) {
    console.log("mixed_highlight")
    data.type = 1009;
    // extraType;uuid num;param num;bldg_id;[low_limit];[high_limit];direction
    // data.uuid = "1;3;11;f9223715-e6f7-414b-8e77-c6ac067c9af2-00133824;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;7#;1;1;1;1;0;0;0;0;1;0;0"; {
    // data.uuid = "1;3;11;f9223715-e6f7-414b-8e77-c6ac067c9af2-00133824;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;NONE;1;1;1;1;0;0;0;0;1;0;0"; {
    // data.uuid = "1;3;11;None;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;NONE;1;1;1;1;0;0;0;0;1;0;0"; {
    // data.uuid = "1;2;11;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;NONE;0;1;1;1;0;0;0;0;1;0;0"; {
    // data.uuid = "1;2;11;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;NONE;0;1;1;1;0;0;0;0;1;1;0"; {
    // data.uuid = "1;2;11;7fe36e3f-c1e4-4b4a-be7a-d299bcdd231a-001317ac;NONE;0;1;1;1;0;0;0;0;1;1;1"; {
    data.uuid = "1;3;11;model_uuid;area_uuid;building_uuid;0;1;1;1;0;0;0;0;1;1;1"; {
        ws1.send(code(data));
        isrecv = false;
    }
};
// globals
var sss = new Date().getTime();
var wsServer1 = 'ws://172.16.201.184:10148';
// var wsServer1 = 'ws://127.0.0.1:9080';

var ws1;
ws1 = new WebSocket(wsServer1);
ws1.onopen = function(evt) {
    onOpen1(evt)
};
ws1.onclose = function(evt) {
    onClose1(evt)
};
ws1.onmessage = function(evt) {
    onMessage1(evt)
};
ws1.onerror = function(evt) {
    onError1(evt)
};

function onOpen1(evt) {
    console.log("连接服务器9003成功");
    // var data = {}
    data.type = 1;
    data.dx = 0;
    data.dy = 0;
    data.posx = 0;
    data.posy = 0;
    data.uuid = 'userid';

    // ws1.send(JSON.stringify(data));
    ws1.send(code(data));

    data.type = 500;
    ws1.send(code(data));
}


function onClose1(evt) {
    //console.log("Disconnected");
}

function onError1(evt) {
    //console.log('Error occured: ' + evt.data);
}

function arrayBuffer2String(buffer) {
    var dv = new DataView(buffer);
    var uuid = [];
    for (i = 0; i < buffer.byteLength; i++) {

        uuid.push(String.fromCharCode(dv.getInt8(i)));
    }
    return uuids = uuid.join("");

}
function hightlightBoxBuildNumber(bn){
    data.type = 1066;
    data.uuid = '{"ldArr":[{"objects":["'+bn+'"],"objectType":"buildNumber","type":"boxHighlight","highlightColor":"ff0000","opacity":"0.5"}]}';
    ws1.send(code(data));
}


var draw_navi_image = false;

function doJsonDataParseOper(buffer) {
    var sz_data = arrayBuffer2String(buffer);
    sz_data = decodeURIComponent(sz_data);
    console.log("sz_data:"+sz_data);
    var obj_js2 = JSON.parse(sz_data);
    var js_type = obj_js2["type"];
    console.log("js_type:"+js_type);
    if("SelectedUUid" == js_type){
        selected_uuid = obj_js2["message"];
    }else if ("GreenLine" == js_type) {
        var pos1 = obj_js2["positions"]["pos1"];
        posx = pos1.split(",")[0]
        posy = pos1.split(",")[1]
            // console.log("x: ", posx, " y: ", posy)
    }else if("two_mesh_dist" == js_type){
        first_point.x = obj_js2["first_point"][0];
        first_point.y = obj_js2["first_point"][1];
        second_point.x = obj_js2["second_point"][0];
        second_point.y = obj_js2["second_point"][1];
        if(first_point.x >=0 && first_point.y>=0 && second_point.x >= 0 && second_point.y >= 0){
            two_mesh_dist = true;
            updateMeasuring();
        }
    }else if ("linesOrAreasMeasure" == js_type) {
        measur_type = "linesOrAreasMeasure";
        measur_list.count = obj_js2.count;
        console.log("data count: ", measur_list.count);
        measur_list.data = obj_js2.data;
        console.log("data len: ", measur_list.data.length);
        updateMeasuring();
    }else if("OutputNavPos" == js_type) {
        //导航图图标：三角和圆。
        uuid = obj_js2["message"];
        reDrawNavigationPoint(uuid);
    }else if("OutputNavChart" == js_type) {
        uuid = obj_js2["message"];
        if(uuid != "navigationChart")
        {
            console.log("Error: OutputNavChart message:"+ uuid);
        }
        else
        {
            draw_navi_image = true;
        }
    }else if("backline_check" == js_type){
        var bn_list = obj_js2.bn_list;
        if(bn_list.length == 0)
        {
            console.log("backline check ok!");
        }
        else
        {
            for(i = 0;i<bn_list.length;i++)
            {
                var bn = bn_list[i];
                hightlightBoxBuildNumber(bn);
            }
        }
    }else if ("linesMeasure" == js_type) {
        measur_type = "linesMeasure";
        lines_measure_data.count = obj_js2.count;
        if(obj_js2.hasOwnProperty("lastScreenPosx"))
        {
            lines_measure_data.has_last = true;
            lines_measure_data.last_x = obj_js2.lastScreenPosx;
            lines_measure_data.last_y = obj_js2.lastScreenPosy;
        }
        else
        {
            lines_measure_data.has_last = false;
        }
        lines_measure_data.data = obj_js2.data;
        updateMeasuring();
    }else{
        console.log("no handle json:"+js_type);
    }
}

function drawPointMark(x,y){
    //console.log("draw mark:"+x+","+y);
    ctx.strokeStyle = "blue";
    ctx.beginPath();
    ctx.moveTo(x,y+5);
    ctx.lineTo(x+5,y);
    ctx.lineTo(x,y-5);
    ctx.lineTo(x-5,y);
    ctx.lineTo(x,y+5);
    ctx.closePath();
    ctx.stroke();
}
function drawLine(x1,y1,x2,y2){
    //console.log("draw line.")
    ctx.strokeStyle = "red";
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.closePath();
    ctx.stroke();
}
function updateMeasuring()
{
    //console.log("measuring:"+measuring+",measur_list.data.length:"+measur_list.data.length);
    if(measuring){
        if(measur_type == "linesOrAreasMeasure")
        {
            for(var i = 0; i < measur_list.data.length; i++){
                var la = measur_list.data[i];
                var la_point_list = la.list;
                var pre_x = -1;
                var pre_y = -1;
                for(var j = 0; j < la_point_list.length; ++j){
                    var pt = la_point_list[j]
                    var x = Number(pt["screenPosx"]);
                    var y = Number(pt["screenPosy"]);
                    var dist = Number(pt["distance"]);
                    drawPointMark(x,y);
                    if(pre_x > 0 && pre_y > 0 && x > 0 && y > 0){
                        drawLine(pre_x, pre_y, x, y);
                    }
                    pre_x = x;
                    pre_y = y;
                }
            }
        }
        else if(measur_type == "linesMeasure")
        {
            if(lines_measure_data.has_last)
            {
                var x = Number(lines_measure_data.last_x);
                var y = Number(lines_measure_data.last_y);
                drawPointMark(x,y);
            }
console.log("lines_measure_data len:",lines_measure_data.data.length);
            for(var i = 0; i < lines_measure_data.data.length; i++)
            {
                var line = lines_measure_data.data[i];
                var x1 = Number(line.screenPosx1);
                var y1 = Number(line.screenPosy1);
                var x2 = Number(line.screenPosx2);
                var y2 = Number(line.screenPosy2);
                drawPointMark(x1,y1);
                drawPointMark(x2,y2);
                drawLine(x1,y1,x2,y2);
            }
        }
    }
    else if(two_mesh_dist){
        drawLine(first_point.x,first_point.y,second_point.x, second_point.y);
    }
}

function isJpeg(flag){
    return (flag == -520103681 )
}

function drawJpeg(blob,start){
    var imgUrl = URL.createObjectURL(blob.slice(start));
    img.src = imgUrl;
    img.onload = function() {
        ctx.drawImage(img, 0, 0, this.naturalWidth, this.naturalHeight, 0, 0, 1280, 720);
        window.URL.revokeObjectURL(imgUrl);
        updateMeasuring();
    };
}

function onMessage1(evt) {
    var s = new Date().getTime();
    console.log("cost===========" + (s - sss));
    sss = s;
    isrecv = true;
    //console.log('Retrieved data from server: ' + evt.data);

    var blob = new Blob([evt.data]);
    var reader = new FileReader();
    reader.addEventListener("loadend", function(e) {
        // reader.result 包含转化为类型数组的blob
        var s = new DataView(reader.result);
        var index_offset = 4;//加了四个字节（uint32）的序号。
        //console.log('s len:'+s.byteLength);
        //console.log('s off:'+s.byteOffset);
        if(s.byteLength == 0)
            return;
        //只有序号。
        if(s.byteLength == index_offset)
            return;
        //console.log("msg len:"+s.byteLength);
        var index = s.getUint32(0, true);
        //console.log("msg index:"+index);
        var flag = s.getInt32(index_offset, true);
        //console.log("flag:",flag);
        var length = 0;
        if(!isJpeg(flag)){
            length = s.getInt32(index_offset, true);
            var retype = arrayBuffer2String(reader.result.slice(index_offset+4, index_offset+8));
        }
        var image_offset = index_offset + 4 + length;    //jpeg图片的偏移。lenghth = "json"4+json长度。
        var json_offset = index_offset + 4 + 4;         //json字符串偏移：index(4),size(4),"json"(4). size为“json”4个标志字符+json字符串的长度。
        //console.log(retype);
        if (isJpeg(flag))
        {
            //仅jpeg。
            drawJpeg(blob, index_offset);
        }
        else
        {
            if(retype == "json")
            {
                doJsonDataParseOper(reader.result.slice(json_offset, image_offset));
            }
            else    //导航图还使用uuid形式返回字符串内容。
            {
                //看看是否有不是json的数据。
                reuuid = reader.result.slice(index_offset + 4, image_offset);
                var sz_data = arrayBuffer2String(reuuid);
                console.log("Not json:",sz_data);
            }
            //先绘制jpeg。
            if(s.byteLength>image_offset){
                if(isJpeg(s.getInt32(image_offset,true))){
                    if(!draw_navi_image)
                    {
                        drawJpeg(blob,image_offset);
                    }
                    else
                    {
                        drawNavMapImage(blob,image_offset);
                        draw_navi_image = false;
                    }
                }
            }
        }
    });
    reader.readAsArrayBuffer(blob);
    return;
}

// export { ws1};

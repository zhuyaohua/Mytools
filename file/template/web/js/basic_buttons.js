
function reset() {
    data.posx = 0;
    data.posy = 0;

    data.type = 30;
    data.dx = 0;
    data.dy = 0;
    ws1.send(code(data));
}

document.getElementById("btnReset").onclick = function (e) {
    console.log("reset")
    reset();
};

document.getElementById("show").onclick = function (e) {

        data.posx = 0;
        data.posy = 0;

        data.type = 11;
        data.dx = 0;
        data.dy = 0;

        {
            ws1.send(code(data));
            isrecv = false;
        }
};

document.getElementById("hide").onclick = function (e) {

        data.posx = 0;
        data.posy = 0;

        data.type = 12;
        data.dx = 0;
        data.dy = 0;	
        data.uuid = selected_uuid;
        console.log(data.uuid)
        {
            ws1.send(code(data));
            isrecv = false;
        }
};

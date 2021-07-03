var ws1_bak;
var data_bak;

// var ws1;

var isConnect = false,
    isDown = false,
    isUp = false,
    isrecv = true;
batchselect = 0;
shadow = false;
outline = 0;
cullbox = false;
doFrameSelection = false;
cullboxMouseDown = 80;
var ctrlkey = false,
    shiftkey = false;
var measuring = false;
var measur_type = "";
var multAreaSelect = false;
var attractive = false;
var x, y = 0;

var marking = false;

var measur_list ={};
measur_list.type = "linesOrAreasMeasure";
measur_list.count = 0;
measur_list.data = new Array();

var lines_measure_data ={};

lines_measure_data.has_last = false;
lines_measure_data.last_x = 0;
lines_measure_data.last_y = 0;
lines_measure_data.count = 0;
lines_measure_data.data = new Array();


var ctx = document.getElementById('showcanvas').getContext('2d')
var img = new Image()


var reuuid;
var data = {};
data.type = 0;
data.extraType = 0;
data.dx = 0;
data.dy = 0;;
data.posx = 0;
data.posy = 0;
data.anx = 0;
data.asx = 0;
data.any = 0;
data.asy = 0;
data.anz = 0;
data.asy = 0;
data.uuid = '';
ws1_bak = ws1;
data_bak = data;
var isClickCanvas = false;

// GreenLine
var posx, posy;

// two mesh distance display.
var first_point = {}
var second_point = {}
first_point.x = 0;
first_point.y = 0;
second_point.x = 0;
second_point.y = 0;
var two_mesh_dist = false;

var selected_uuid = '';

var catchNearPoint = false;//91,0,吸附端点。
var catchNearPointType = 4;// 1 sidepoint ; 2 midpoint ; 3 footpoint ; 4 allpoints .

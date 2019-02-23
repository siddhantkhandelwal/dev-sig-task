$('#Blocks g').addClass('blocks');
for(var ii = 1; ii < 5; ii++){
    $(`#Group${ii} > g`).addClass(`group ${ii}`);
}


function getValue(element, property, units) { // property can only be x or y or height or width
    // returns properties in absolute values
    // origin is set to bottom left corner
    if (property == 'x') {
        return parseFloat(element.getAttribute('transform').split('translate(').join(',').split(')').join(',').split(',')[1]); // 6720 is viewport width of svg
    }
    if (property == 'y') {
        return parseFloat(element.getAttribute('transform').split('translate(').join(',').split(')').join(',').split(',')[2]); // 480 is viewport height of svg       
    }
}

function getValueBlock(element, property) {
    
    if (property == 'height') {
        return (16 * 100 / 480);
    }
    if (property == 'width') {
        return (16 * 100 / 6720);
    }
    if (property == 'x') {
        return (getValue(document.getElementById('Blocks'), 'x', '%') + getValue(element,'x',"%"))*100/6720;
    }
    if (property == 'y') {
        return (480 - getValue(document.getElementById('Blocks'), 'y', 'vh' )- getValue(element,'y','vh')) * 100 / 480;
    }
}

function getValueGroup(element, property) {
    var group_num = parseInt(element.classList[1]);
    if (property == 'height') {
        if(element.id == 'PipeSmall'){
            return (32*100/480);
        }
        else if(element.id == 'PipeMedium'){
            return (48*100/480);
        }
        else if(element.id == 'PipleLarge'){
            return (64*100/480);
        }
        else return (16 * 100 / 480);
    }
    if (property == 'width') {
        if(element.id == 'PipeSmall' || element.id == 'PipeMedium' || element.id == 'PipleLarge'){
            return 32*100/6720;
        }
        else return 16 * 100 / 6720;
    }
    if (property == 'x') {
        return (getValue(document.getElementById(`Group${group_num}`), 'x', '%') + getValue(element,'x','%')) * 100 / 6720;
    }
    if (property == 'y') {
        return (480 - getValue(document.getElementById(`Group${group_num}`), 'y', 'vh') - getValue(element,'y','vh')) * 100 / 480;
    }
}

var rest_left = [];
var rest_top = [];

var blocks_svg = document.getElementsByClassName("blocks");
for (var ii = 0; ii < blocks_svg.length; ++ii) {
    var temp = {
        "element": blocks_svg[ii],
        "left": getValueBlock(blocks_svg[ii], 'x'),
        "top": getValueBlock(blocks_svg[ii], 'y'),
        "height": getValueBlock(blocks_svg[ii], 'height'),
        "width": getValueBlock(blocks_svg[ii], 'width'),
    };
    temp.right = temp.left + temp.width;
    temp.bottom = temp.top - temp.height;
    rest_left.push(temp);
}
var groups_svg = document.getElementsByClassName("group");
for (var ii = 0; ii < groups_svg.length; ++ii) {
    var temp = {
        "element": groups_svg[ii],
        "left": getValueGroup(groups_svg[ii], 'x'),
        "top": getValueGroup(groups_svg[ii], 'y'),
        "width": getValueGroup(groups_svg[ii], 'width'),
        "height": getValueGroup(groups_svg[ii], 'height')
    };
    temp.right = temp.left + temp.width;
    temp.bottom = temp.top - temp.height;
    rest_left.push(temp);
}
rest_left.sort(function(a, b) {     // left to right then top to bottom
    if(a.left == b.left){return b.top - a.top;}
    return a.left - b.left;
}) // left to right

for (var jj = 0; jj < rest_left.length; ++jj) {
    rest_top.push(rest_left[jj]);
}
rest_top.sort(function(a, b) {      // top to bottom then left to right
    if(b.top == a.top){return a.left - b.left;}
    else return b.top - a.top;
}) // top to bottom

var mario = {"element": document.getElementById("mario")};
mario.width =  14*100/6720;
mario.height = 16*100/480;
mario.left = getValue(mario.element, 'x','%')*100/6720;
mario.top = (480 - getValue(mario.element, 'y',"vh"))*100/480;
mario.right = mario.left + mario.width;
mario.bottom = mario.top - mario.height;
mario.defaultbottom = (480 - 432)*100/480 - mario.height;

function updateMario(){
    mario.left = getValue(mario.element, 'x','%')*100/6720;
    mario.top = (480 - getValue(mario.element, 'y',"vh"))*100/480;
    mario.right = mario.left + mario.width;
    mario.bottom = mario.top - mario.height;
}

var game = document.getElementById("game");         // game is the entire svg wrapper


function setSvgAttribute(element, attributeName, attributeValue) {
    element.setAttribute(attributeName, attributeValue);
}

// NOTE: GIVE CO-ORDS FOR !TOP! AND LEFT
function transformSvgElement(element, x, y) {
    x = x*6720/100;
    y = 480 - (y*480/100);
    setSvgAttribute(element, 'transform', 'translate(' + x + ', ' + y + ' )');
    updateMario();
}
var flag_up = true;
// var jump_dur = parseFloat(window.getComputedStyle(mario).getPropertyValue("transition-duration"))*1000;    //in ms

function stay() {
    for (var ii = 0; ii < rest_top.length; ii++) {
        if (mario.bottom >= (rest_top[ii].top-0.01) && mario.left < rest_top[ii].right && mario.right > rest_top[ii].left) {
            return ii; // checks  in descending order
        }
    }
    return -1;
}
/***************************************************************/

/******can be changed variables**********/
var jump_dur = 200;        //ms
var speed_rel = 0.1;      //percentage of 6720
var jump_height = 15;     //percentage of 480

/******derived variables **********/
var actualwidth = $('#mainsvg').width();
var ratio = actualwidth/6720; //change to get width
var defaultleft = 177*100/6720;
var endingleft = (1 - (0.83*window.innerWidth)/actualwidth)*100;
var speed = (speed_rel*6720/100)*ratio;              //pixels
var pixelx = 0;
var direction = 1; // not used rn
var key_left = false;
var key_right = false;
var jumping = false;

var marioright = document.getElementById("marioright");
var marioleft = document.getElementById("marioleft");

/***************************************************************/
function handleKeyDown(event) {
    if (event.keyCode == 37){
        key_left = true;
        marioleft.classList.remove("hidden");
        marioright.classList.add("hidden");
    }
    else if (event.keyCode == 39){
        key_right = true;
        marioleft.classList.add("hidden");
        marioright.classList.remove("hidden");
    }
    moveSide();
}

function handleKeyUp(event) {
    if (event.keyCode == 37)
        key_left = false;
    else if (event.keyCode == 39)
        key_right = false;
}

function onb() { //checks if on block and moves char down if reqd
    if (stay() != -1) {
        transformSvgElement(mario.element,mario.left,rest_top[stay()].top + mario.height);
    } else if(stay() == -1){
        transformSvgElement(mario.element,mario.left,mario.defaultbottom + mario.height);
    }
}
var falling;
var ques = document.getElementById('ques');
var cross = document.getElementById('Notnot');
var background = document.getElementById('bgrd');
var i;
function moveUp(e) {
    if(bgrd.className == 'hideBox '){
        e = e || window.event;
        if (e.keyCode == '38' && key_left != true && key_right!=true) {
            window.removeEventListener("keydown", moveUp);
            clearTimeout(falling);
            flag_up = false;
            // up arrow
            var flag = 0;
            jump_start: {
                for (var ii = rest_top.length - 1; ii > -1; --ii) //ascending order
                {
                    if ((mario.left < rest_top[ii].right) && (mario.right > rest_top[ii].left)){
                        if(rest_top[ii].bottom - mario.top <= jump_height && mario.top < rest_top[ii].bottom)
                        {   
                            flag = 1;
                            transformSvgElement(mario.element,mario.left,rest_top[ii].bottom);
                            if (rest_top[ii].element.id == 'CoinBlock'){
                                // questionpopup();
                                var key = rest_top[ii].element.getAttribute('key');
                                // console.log(key);
                                var data = getQuestion(key);
                                var text = JSON.stringify(data);
                                // console.log(text);
                                // console.log(data);
                                if(rest_top[ii].element.style.display != 'none'){
                                    questionpopup();
                                }
                            }
                            break jump_start;
                        }
                    }
                }
            }
            if (flag == 0) {
                transformSvgElement(mario.element,mario.left,mario.bottom + mario.height + jump_height);
                $('#mario').toggleClass('marioJumpAnim');
            };
            setTimeout(function() {
                window.addEventListener("keydown", moveUp);
                flag_up = true
            }, (2 * jump_dur) - (jump_dur / 20));
        }
        if (e.keyCode == '38' && key_left == true && key_right!=true) {
            window.removeEventListener("keydown", moveUp);
            clearTimeout(falling);
            flag_up = false;
            // up arrow
            var flag = 0;
            jump_start: {
                for (var ii = rest_top.length - 1; ii > -1; --ii) //ascending order
                {
                    if (mario.left < rest_top[ii].right && mario.right > rest_top[ii].left){
                        if(rest_top[ii].bottom - mario.top <= jump_height && mario.top < rest_top[ii].bottom)
                        {   
                            flag = 1;
                            pixelx = speed_rel*jump_dur/50;
                            // transformSvgElement(mario.element,mario.left - pixelx,rest_top[ii].bottom);
                            // game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) + ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                            if((mario.left - pixelx) <= 2*100/6720)
                            {
                                transformSvgElement(mario.element,2*100/6720,rest_top[ii].bottom);
                            }
                            else {
                                transformSvgElement(mario.element,mario.left - pixelx,rest_top[ii].bottom);
                            }
                            if(mario.left >= defaultleft && mario.left < endingleft){
                                game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left'))) + ((pixelx*6720/100)*ratio) + 'px';         // in pixels here
                            }
                            if (rest_top[ii].element.id == 'CoinBlock'){
                                var key = rest_top[ii].element.getAttribute('key');
                                // console.log(key);
                                var data = getQuestion(key);
                                var text = JSON.stringify(data);
                                // console.log(text);
                                // console.log(data);
                                if(rest_top[ii].element.style.display != 'none'){
                                    questionpopup();
                                }
                            }
                            break jump_start;
                        }
                    }
                }
            }
            if (flag == 0) {
                pixelx = speed_rel*jump_dur/100;
                // transformSvgElement(mario.element,mario.left - speed_rel*jump_dur/100,mario.bottom + mario.height + jump_height);
                // game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) + ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                if((mario.left - pixelx) <= 2*100/6720)
                {
                    transformSvgElement(mario.element,2*100/6720,mario.top + jump_height);
                }
                else {
                    transformSvgElement(mario.element,mario.left - pixelx,mario.top + jump_height);
                }
                if(mario.left >= defaultleft && mario.left < endingleft){
                    game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left'))) + ((pixelx*6720/100)*ratio) + 'px';         // in pixels here
                }
            };
            setTimeout(function() {
                window.addEventListener("keydown", moveUp);
                flag_up = true
            }, (2 * jump_dur) - (jump_dur / 20));
        }
        if (e.keyCode == '38' && key_left != true && key_right == true ) {
            window.removeEventListener("keydown", moveUp);
            clearTimeout(falling);
            flag_up = false;
            // up arrow
            var flag = 0;
            jump_start: {
                for (var ii = rest_top.length - 1; ii > -1; --ii) //ascending order
                {
                    if (mario.left < rest_top[ii].right && mario.right > rest_top[ii].left){
                        if(rest_top[ii].bottom - mario.top <= jump_height && mario.top < rest_top[ii].bottom)
                        {   
                            flag = 1;
                            pixelx = speed_rel*jump_dur/100;
                            // transformSvgElement(mario.element,mario.left + pixelx,rest_top[ii].bottom);
                            // game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) - ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                            if(mario.left + pixelx >= 6500*100/6720)
                            {
                                transformSvgElement(mario.element,6500*100/6720,rest_top[ii].bottom);
                            }
                            else 
                                transformSvgElement(mario.element,mario.left + pixelx,rest_top[ii].bottom);
                            if(mario.left >= defaultleft && mario.left < endingleft){
                                game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) - 
                                ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                            }
                            if (rest_top[ii].element.id == 'CoinBlock'){
                                var key = rest_top[ii].element.getAttribute('key');
                                // console.log(key);
                                var data = getQuestion(key);
                                var text = JSON.stringify(data);
                                // console.log(text);
                                // console.log(data);
                                if(rest_top[ii].element.style.display != 'none'){
                                    questionpopup();
                                }
                            }
                            break jump_start;
                        }
                    }
                
                }
            }
            if (flag == 0) {
                pixelx = speed_rel*jump_dur/100;
                // transformSvgElement(mario.element,mario.left + speed_rel*jump_dur/100,mario.bottom + mario.height + jump_height);
                // game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) - ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                if(mario.left + pixelx >= 6500*100/6720)
                {
                    transformSvgElement(mario.element,6500*100/6720,mario.top + jump_height);
                }
                else 
                    transformSvgElement(mario.element,mario.left + pixelx,mario.top + jump_height);
                if(mario.left >= defaultleft && mario.left < endingleft){
                    game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) - 
                    ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
                }
            };
            setTimeout(function() {
                window.addEventListener("keydown", moveUp);
                flag_up = true
            }, (2 * jump_dur) - (jump_dur / 20));
        }
        falling = setTimeout(onb, jump_dur - (jump_dur / 20)); // called for any key press.

    }
}

function moveDown(e) {
    if (e.keyCode == '40') {
        // down arrow
        if (flag_up == false) {
            flag_up = true;
            window.addEventListener("keydown", moveUp);
        }
        if (stay() != -1) {
            transformSvgElement(mario.element,mario.left,rest_top[stay()].top + mario.height);
        } 
        else transformSvgElement(mario.element,mario.left,mario.defaultbottom + mario.height);
    }
}


function check_right() {
    for (var ii = 0; ii < rest_left.length; ++ii) {
        var b_left = rest_left[ii].left - speed_rel;
        if (mario.right > b_left && mario.right < (b_left + rest_left[ii].width)) {
            if ((mario.top < rest_left[ii].top && mario.top >= rest_left[ii].bottom) || (mario.bottom < rest_left[ii].top && (mario.bottom > (rest_left[ii].bottom - 0.01)))) {
                    return ii;
            }
        }
    }
    return -1;
}

function check_left() {
    for (var ii = rest_left.length - 1; ii >= 0; --ii) {
        var b_right = rest_left[ii].right + speed_rel;
        if (mario.left < b_right && mario.left > (b_right - rest_left[ii].width)) {
            if ((mario.top < rest_left[ii].top && mario.top >= rest_left[ii].bottom) ||
            (mario.bottom < rest_left[ii].top && (mario.bottom > (rest_left[ii].bottom-0.01))))
                return ii;
        }
    }
    return -1;
}
function moveSide() {
    if(bgrd.className == 'hideBox '){
    if (key_left == true) {
        // left arrow
        if (check_left() == -1) {
            pixelx += speed_rel;
        } else pixelx += mario.left - rest_left[check_left()].right;
        if(pixelx > speed_rel){pixelx = speed_rel;}
        if(mario.left - pixelx <= 2*100/6720)
        {
            transformSvgElement(mario.element,2*100/6720,mario.bottom+mario.height);
        }
        else 
            transformSvgElement(mario.element,mario.left - pixelx,mario.bottom + mario.height);
        if(mario.left >= defaultleft && mario.left <= endingleft){
            game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left'))) + ((pixelx*6720/100)*ratio) + 'px';         // in pixels here
        }
        pixelx = 0;
    }

    if (key_right == true) {
        // right arrow
        if (check_right() == -1) {
            pixelx += speed_rel;
        } else pixelx += (rest_left[check_right()].left - mario.right);
        if(pixelx > speed_rel){pixelx = speed_rel;}
        if(mario.left + pixelx >= 6500*100/6720)
        {
            transformSvgElement(mario.element,6500*100/6720,mario.bottom+mario.height);
        }
        else 
            transformSvgElement(mario.element,mario.left + pixelx,mario.bottom + mario.height);
        if(mario.left >= defaultleft && mario.left <= endingleft){
            game.style.left = (parseFloat(window.getComputedStyle(document.getElementById("game")).getPropertyValue('left')) - 
            ((pixelx*6720/100)*ratio)) + 'px';             // in pixels here
        }
        pixelx = 0;
    }
}
}

window.addEventListener("keydown", moveUp);
window.addEventListener("keydown", moveDown);
window.addEventListener("keydown", handleKeyDown);
window.addEventListener("keyup", handleKeyUp);
window.addEventListener("keydown", closeqn);

/*document.addEventListener('keydown', function abc(event) {
    if (event.keyCode == 73 ) {//just change the event listeneer to the conditions
        //of collisions.*/
function questionpopup() {
        bgrd.className += ' modalBackground';
        ques.className += ' questionBox';
    //     function typeEffect(element, speed) {
    //     var text = $(element).text();
    //     $(element).html('');
    //     i = 0;
    //     var timer = setInterval(function() {
    //                     if (i < text.length) {
    //                         $(element).append(text.charAt(i));
    //                         i++;
    //                     } else {
    //                         clearInterval(timer);
    //                     }
    //                 }, speed);
    //     }

    // $( document ).ready(function() {
    //     var speed = 0.1;
    //     var delay = $('h1').text().length * speed + speed;
    //     typeEffect($('h1'), speed);
    //     setTimeout(function(){
    //     $('p').css('display', 'inline-block');
    //     typeEffect($('p'), speed);
    //     }, delay);
    //     });
}

var press_submit = document.getElementById('submit1');

press_submit.addEventListener('click', function closepopup(event){
    ques.className = 'hideBox ';
    bgrd.className = 'hideBox ';
});

cross.addEventListener('click', function bcd(event) {//close the pop-up
    ques.className = 'hideBox ';
    bgrd.className = 'hideBox ';
});

$('#answerForm').submit(function(event) {
    // console.log(  $('.answerTextField').val());
    window.setTimeout(function() {
    var scoreContainer = document.getElementById('score');
    var currentScore = scoreContainer.innerHTML;
    getScore();
    window.setTimeout(() => {
        var newScore = scoreContainer.innerHTML;
        if( currentScore > newScore) {
            alert('Answer is wrong');
        }
        else if( currentScore < newScore) {
            alert("Congrats! You've answered correctly");
        }
    },200);
    // console.log(newScore);
    // console.log(currentScore);
    getCorrectQuestions();
    }, 3000);
});

function getQuestion(key){   
    document.getElementById('p1').innerHTML = "";

    // console.log($('.answerTextField').val())
    $('.answerTextField').val('');

    var data = $.ajax( {
        type: 'POST',
        url: '/game/',
        data: {
            'questionKey': key
        },
        success: function(data) {
            // console.log(data);
            var obj = JSON.parse;
            var x = data.question_text;
            // console.log(x);
            document.getElementById('question').innerHTML = x;
            // console.log(document.getElementById('question').innerHTML);
                     
        }
        
    });
    return data;
}

//If the below time interval is made shorter, an error occurs - which affects the question text. DO NOT CHANGE THE TIME INTERVAL. I suggest calling the getScore function through an event listener instead.

// window.setInterval(getScore, 3000); //I'm updating score every 1000 milliseconds because I have no clue how event listeners work. Someone from front end please un-idiotify this code.
function getScore(){
    var data = $.ajax( {
        type: 'GET',     //I had written POST here by mistake and it took me two fucking hours to figure out the bug javascript is evil I hate it.
        url: '/display_score/',
        data: {
            'questionKey': 1
        },
        success: function(data) {
            var obj = JSON.parse;
            var x = data.score;  
            document.getElementById('score').innerHTML = x;                     
        }
        
    });
    return data;
}
var GlobalTime;
    var data = $.ajax( {
        type: 'GET',    
        url: '/time/',
        data: {},
        success: function(data) {
            var obj = JSON.parse;
            GlobalTime = data.time;
            // console.log(GlobalTime);
            document.getElementById('timeleft').innerHTML = GlobalTime + " min";     
        }
        
    });

window.setInterval(function reducetime(){
    // console.log(GlobalTime);
    GlobalTime = GlobalTime - 1;
    document.getElementById('timeleft').innerHTML = GlobalTime + " min";
},60000);

// window.setInterval(getCorrectQuestions, 3000)
function getCorrectQuestions(){
    var data = $.ajax( {
        type: 'GET',     
        url: '/get_question_list',
        data: {},
        success: function(data) {
            var obj = JSON.parse;
            var x = data.correct_list;
            // console.log(x);
            for(var p = 0 ; p < x.length ; p ++){
                var demo = x[p];
                // console.log(demo);

            var questionBlock = $('[key=' +  demo + ']');
            // console.log(questionBlock);
            questionBlock.css('display', 'none');
            }
        }


    });
    return data;
}

getCorrectQuestions();
getScore();


function closeqn(e){
    if (e.keyCode == 27)
    {
        ques.className = 'hideBox ';
        bgrd.className = 'hideBox ';
    }
}
// function post(path, params, method) {
//     method = method || "post"; // Set method to post by default if not specified.

//     // The rest of this code assumes you are not using a library.
//     // It can be made less wordy if you use one.
//     var form = document.createElement("form");
//     form.setAttribute("method", method);
//     form.setAttribute("action", path);

//     for(var key in params) {
//         if(params.hasOwnProperty(key)) {
//             var hiddenField = document.createElement("input");
//             hiddenField.setAttribute("type", "hidden");
//             hiddenField.setAttribute("name", key);
//             hiddenField.setAttribute("value", params[key]);
//             //hiddenField.setAttribute();

//             form.appendChild(hiddenField);
            
//         }
//     }

//     document.body.appendChild(form);
//     form.submit();
// }
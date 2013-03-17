    function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}

function dataURItoArrayBuffer(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Uint8Array(array);
}

// LZW-compress a string
function lzw_encode(s) {
    var dict = {};
    var data = (s + "").split("");
    var out = [];
    var currChar;
    var phrase = data[0];
    var code = 256;
    for (var i=1; i<data.length; i++) {
        currChar=data[i];
        if (dict[phrase + currChar] != null) {
            phrase += currChar;
        }
        else {
            out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
            dict[phrase + currChar] = code;
            code++;
            phrase=currChar;
        }
    }
    out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
    for (var i=0; i<out.length; i++) {
        out[i] = String.fromCharCode(out[i]);
    }
    return out.join("");
}


// Decompress an LZW-encoded string
function lzw_decode(s) {
    var dict = {};
    var data = (s + "").split("");
    var currChar = data[0];
    var oldPhrase = currChar;
    var out = [currChar];
    var code = 256;
    var phrase;
    for (var i=1; i<data.length; i++) {
        var currCode = data[i].charCodeAt(0);
        if (currCode < 256) {
            phrase = data[i];
        }
        else {
           phrase = dict[currCode] ? dict[currCode] : (oldPhrase + currChar);
        }
        out.push(phrase);
        currChar = phrase.charAt(0);
        dict[code] = oldPhrase + currChar;
        code++;
        oldPhrase = phrase;
    }
    return out.join("");
}

function conenct(){
        var socket;
        var host="ws://192.168.1.127:9999";
        
        socket=new WebSocket(host);

        socket.onopen = function () {
              console.log("Openened connection to websocket");
        };

        socket.onerror = function(error){
            console.log('WebSocket Error' + error);
         };

        socket.onmessage=function(e){
            console.log('Server: '+e.data);
        };

    }


     $(document).ready(function() {

        

    //Compatibility
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;

    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        video = document.getElementById("video"),
        btnStart = document.getElementById("btnStart"),
        btnStop = document.getElementById("btnStop"),
        btnPhoto = document.getElementById("btnPhoto"),
        videoObj = {
            video: true,
            audio: true
        };
        window.socket;
        window.host="ws://192.168.1.127:9000";
        window.oFile=new FileReader();
        window.frameCounter=1;
        window.packetCount=0;
        window.globaljson={};
        window.maxFrames=750;

        oFile.onload = function (oFREvent){
/*            if (maxFrames>=frameCounter){
                globaljson[frameCounter.toString()]=btoa(oFREvent.target.result);
                ++frameCounter;
            }
            else{
                tmp=JSON.stringify(globaljson); 
                a=tmp.length;
                b=lzw_encode(tmp).length;
            }
*/


            var jsonObj={};
                jsonObj["frame"]=frameCounter;
                jsonObj["user"]="Harnek";
                jsonObj["payload"]=btoa(oFREvent.target.result);
                tmp=JSON.stringify(jsonObj);
              //  o=tmp.length;
             //   tk=lzw_encode(tmp);
              //  p=tk.length;
                socket.send(tmp);
                ++frameCounter;
/*

                globaljson[packetCount.toString()]=jsonObj;
                ++frameCounter;
                ++packetCount;

                if(packetCount>=2){
                    packetCount=0;
                    globaljson["user"]="Harnek";    
                    tmp=JSON.stringify(globaljson);   
                    tk=lzw_encode(tmp);
                    m=tmp.length;   
                    l=tk.length;       
                    socket.send(tmp);
                    globaljson={};
                } */
        };
        
        socket=new WebSocket(host);

        socket.onopen = function () {
              console.log("Openened connection to websocket");
        };

        socket.onerror = function(error){
            console.log('WebSocket Error' + error);
         };

        socket.onmessage=function(e){
            console.log('Server: '+e.data);
        };

    btnStart.addEventListener("click", function() {
        var localMediaStream;

        if (navigator.getUserMedia) {
            navigator.getUserMedia(videoObj, function(stream) {              
                video.src = (navigator.webkitGetUserMedia) ? window.webkitURL.createObjectURL(stream) : stream;
                localMediaStream = stream;
                
            }, function(error) {
                console.error("Video capture error: ", error.code);
            });

            btnStop.addEventListener("click", function() {
                localMediaStream.stop();
            });

            btnPhoto.addEventListener("click", function() {
                context.drawImage(video, 0, 0, 320, 240);

            });
            frameCounter=1;
            timer = setInterval(
            function () {
                context.drawImage(video, 0, 0, 640, 480);
                var data = $("#canvas").get()[0].toDataURL('image/jpeg', 0.5);
                newblob = dataURItoBlob(data);

                var target = document.getElementById("target");
                var url=url=window.webkitURL.createObjectURL(newblob);
                target.src=url;
                oFile.readAsBinaryString(newblob);
            }, 33);
        }
    });

        });

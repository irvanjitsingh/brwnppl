function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}


$(document).ready(function() {
        //Compatibility
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;

    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        video = document.getElementById("video"),
        btnStart = document.getElementById("btnStart"),
        btnStop = document.getElementById("btnStop"),
        btnRecord = document.getElementById("btnRecord"),
        videoObj = {
            video: true,
            audio: true
        };
    window.socket=null;
    window.host="ws://192.168.1.127:9000";
    window.oFile=new FileReader();
    window.frameCounter=1;
    window.videoTimer=null;

    oFile.onload = function (oFREvent){

        var jsonObj={};
        jsonObj["frame"]=frameCounter;
        jsonObj["user"]="Harnek";
        jsonObj["payload"]=btoa(oFREvent.target.result);
        tmp=JSON.stringify(jsonObj);
        socket.send(tmp);
        ++frameCounter;
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
                clearInterval(videoTimer);
                localMediaStream.stop();
                socket.close();
                
            });

            btnRecord.addEventListener("click", function() {
                socket=new WebSocket(host);
                socket.onopen = function () {
                    console.log("Openened connection to websocket");
                    videoTimer = setInterval(
                    function () {
                        context.drawImage(video, 0, 0, 640, 480);
                        var data = $("#canvas").get()[0].toDataURL('image/jpeg', 0.5);
                        newblob = dataURItoBlob(data);
                        oFile.readAsBinaryString(newblob);
                    }, 33);
                };

                socket.onerror = function(error){
                  console.log('WebSocket Error' + error);
                 };

                socket.onmessage=function(e){
                    console.log('Server: '+e.data);
                };  

            });
            frameCounter=1;
        }
    });
        

        });
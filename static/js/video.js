function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}
    function stopVideo(event){
        oFile.abort();
        $("btnRecord").unbind("click");
        $("btnStop").unbind("click");

        if (videoTimer){
            clearInterval(videoTimer);                    
        }
        localMediaStream.stop();
        if (socket!=null){
            socket.close();
        }
        video.src="";

        $("#btnStart").bind("click", startVideo);
                
    }

    function recordVideo(event){
        $("#btnRecord").unbind("click");
        socket=new WebSocket(host);
        socket.onopen = function () {
            console.log("Openened connection to websocket");
            videoTimer = setInterval(
            function () {
                context.drawImage(video, 0, 0, 320, 240);
                var data = $("#canvas").get()[0].toDataURL('image/jpeg', 0.2);
                newblob = dataURItoBlob(data);
                oFile.readAsBinaryString(newblob);
            }, 40);
        };

        socket.onerror = function(error){
          console.log('WebSocket Error' + error);
        };

        socket.onmessage=function(e){
            console.log('Server: '+e.data);
        };  
    }

    function startVideo(event){
        $("#btnStart").unbind("click");
        if (navigator.getUserMedia) {
            navigator.getUserMedia(videoObj, function(stream) {     
                $("#btnStart").unbind("click");   
                $("#btnStop").bind("click", stopVideo);
                $("#btnRecord").bind("click", recordVideo);
                video.src = (navigator.webkitGetUserMedia) ? window.webkitURL.createObjectURL(stream) : stream;
                localMediaStream = stream;
                
            }, function(error) {
                console.error("Video capture error: ", error.code);
            });

            frameCounter=1;
        }
    }

     $(document).ready(function() {
        //Compatibility
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;

    window.socket=null;
    window.host="ws://108.171.175.239:9000";
    window.oFile=new FileReader();
    window.frameCounter=1;
    window.videoTimer=null;
    window.maxFrames=250; 

    window.localMediaStream=null;
    window.canvas = document.getElementById("canvas");
    window.context = canvas.getContext("2d");
    window.video = document.getElementById("video");
    window.videoObj = {
            video: true,
            audio: false
        };

    oFile.onload = function (oFREvent){

        var jsonObj={};
        jsonObj["frame"]=frameCounter;
        jsonObj["user"]="Harnek";
        jsonObj["payload"]=btoa(oFREvent.target.result);
        tmp=JSON.stringify(jsonObj);
        socket.send(tmp);
        ++frameCounter;
    };

    $("#btnStart").bind("click", startVideo);

    $("#canvas").css({'visibility':'hidden'});
    });
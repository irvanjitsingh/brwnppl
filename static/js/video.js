function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}
    function sendVideo(event){
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


    function stopVideo(event){
        oFile.abort();
        $("btnRecord").unbind("click");
        $("btnStop").unbind("click");

        if (videoTimer){
            clearInterval(videoTimer);                    
        }
        localMediaStream.stop();
        video.src="";

        $("#btnStart").bind("click", startVideo);
                
    }

    function recordVideo(event){
        $("#btnRecord").unbind("click");
        videoTimer = setInterval(
            function () {
                if (maxFrames>frameCounter){
                    context.drawImage(video, 0, 0, 320, 240);
                    var data = $("#canvas").get()[0].toDataURL('image/jpeg', 0.4);
                    newblob = dataURItoBlob(data);
                    buffer[frameCounter]=newblob;
                    ++frameCounter;
                }
                else{
                    clearInterval(videoTimer);
                    $("btnRecord").unbind("click");
                    $("btnStop").unbind("click");
                    $("#btnStart").unbind("click");
                    if (videoTimer){
                        clearInterval(videoTimer);                    
                    }
                    localMediaStream.stop();
                    video.src="";
                    frameCounter=1;
                    oFile.readAsBinaryString(buffer[frameCounter]);
                } 
            }, 40); 
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
            buffer={};
        }
    }

     $(document).ready(function() {
        //Compatibility
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;

    window.socket=null;
    window.host="ws://184.106.212.32:9000";
    window.oFile=new FileReader();
    window.frameCounter=1;
    window.videoTimer=null;
    window.maxFrames=375;  //*
    window.buffer={}; //* 
    window.jsonObj={};

    window.localMediaStream=null;
    window.canvas = document.getElementById("canvas");
    window.context = canvas.getContext("2d");
    window.video = document.getElementById("video");
    window.videoObj = {
            video: true,
            audio: false
        };

    oFile.onload = function (oFREvent){
        if (maxFrames>frameCounter){
            jsonObj[frameCounter]=btoa(oFREvent.target.result);
            ++frameCounter;
            if (frameCounter==375){
                buffer={};
                frameCounter=1;
                jsonObj["user"]="Harnek";
                tmp=JSON.stringify(jsonObj);
                jsonObj={};
                socket=new WebSocket(host);
                socket.onopen = function () {
                    socket.send(tmp);
                };

                socket.onerror = function(error){
                   console.log('WebSocket Error' + error);
                };

                socket.onmessage=function(e){
                   console.log('Server: '+e.data);
                   if (e.data==0){

                   }
                   else{
                    
                   }
                   /*
                    if (socket!=null){
            socket.close();
        }
        */
                }; 
                
            }
            else{
                oFile.readAsBinaryString(buffer[frameCounter]);
            }
        }
    };

    $("#btnStart").bind("click", startVideo);

    $("#canvas").css({'visibility':'hidden'});
    });
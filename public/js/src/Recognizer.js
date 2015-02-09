var ar = {};


ar.Recognizer = function() {
    // Crate 3d world
    var ui = new ar.ui();

    // Camera poisiton
    ar.ui.Camera.position.z = 0;
    ar.ui.Camera.up = new THREE.Vector3(0, 1, 0);
    ar.ui.Camera.lookAt(new THREE.Vector3(0, 0, 5));

    // Render loop
    var lastRenderedDate = new Date().getTime();
    function render() {
        // Update user skeleton positions if exists
        if (users) {
            for (var user in users) {
                users[user].update();
            }
        }
        
        // Render
        ui.render();

        // Fps
        var fps = parseInt(1000 / ((new Date().getTime()) - lastRenderedDate), 10);
        $('#fps').text('FPS: ' + fps);
        lastRenderedDate = new Date().getTime();

        // Callback
        requestAnimationFrame(render);
    }
    render();

    // Read skeletal data
    var engager = zig.EngageUsersWithSkeleton(4);
    var users = {};
    var maxDisplacementIntervals = {};

    engager.addEventListener('userengaged', function(user) {
        console.log('User engaged: ' + user.id);

        // If skeleton model exits, remove from the scene.
        if (users[user.id])
            users[user.id].removeFromScene();

        // Init
        var maxDisplacement = new ar.SkeletonMaxDisplacement();
        var skeletonArray = [];
        var maxDisplacementIntervalDuration = 1000;
        users[user.id] = new ar.ui.Skeleton(null, { randomColor: true });
     
        function onUserUpdate(user) {
            // Skeletal data is ready.
            users[user.id].skeleton.updateData(user.skeleton);

            // Bindik bi alamete, gidiyoruz kiyamete
            skeletonCopy = new ar.Skeleton(user.skeleton);
            skeletonArray.push(skeletonCopy);
        }

        maxDisplacementIntervals[user.id] = setInterval(function() {
            // Handle max displacement data
            maxDisplacement.updateData(skeletonArray);

            // Handle relative skeleton data
            var lastSkeleton = skeletonArray[skeletonArray.length - 1];
            if (lastSkeleton){
                lastSkeleton.updateSphericalData();
            }

            // Clear skeletons
            skeletonArray = [];

            // Send data to backend for activity recognizing
            socket.emit('recognize', {
                skeleton: lastSkeleton.relativeSphericalData,
                maxDisplacement: maxDisplacement.sphericalData
            }, function (result) {
                var action = null,
                    max = 0;

                for (var actionName in result) {
                    if (result[actionName] > max) {
                        action = actionName;
                        max = result[actionName];
                        
                        var ad = lastSkeleton && lastSkeleton.absoluteData;
                        var t = ad && ad.Torso && ad.Torso.elements;
                        var depth = t && (Math.sqrt(t[0]*t[0] + t[1]*t[1] + t[2]*t[2]));

                        //console.log(ad)
                        var depth_msg = "Torso Distance : " + Math.round((depth*10000))/10000;
                        var action_msg = "Action : " + action;
                        if(depth) {
                            document.getElementById("depth-display").innerHTML = depth_msg; 
                            document.getElementById("action-display").innerHTML = action_msg; 
                        }
                        console.log(depth_msg);
                        console.log(action_msg);
                    }
                }

                // Display recognised action in head label.
                users[user.id].createHeadLabel(action);
            });
        }, maxDisplacementIntervalDuration);

        user.addEventListener('userupdate', onUserUpdate);
        // user.addEventListener('userupdate', _.throttle(onUserUpdate, 1000 / 15));
    });

    engager.addEventListener('userdisengaged', function(user) {
        clearInterval(maxDisplacementIntervals[user.id]);

        // If skeleton model exits, remove from the scene.
        if (users[user.id]) {
            users[user.id].removeFromScene();
            delete users[user.id];
        }

        console.log('User disengaged: ' + user.id);
    });

    zig.addListener(engager);
};

var io,
    self,
    ActivityRecognizer = require('./ActivityRecognizer');
    var net = require('net');
    var fs = require('fs');

/**
 * Socket model constuctor.
 * @constructor
 * @param {Object} opt_server
 */
var SocketModel = function(opt_server) {
    if (self)
        return self;

    self = this;
    this.io = io = require('socket.io')(opt_server);
    this.init();
};


/**
 * Initalize function.
 */
SocketModel.prototype.init = function() {
    var that = this;
    io.on('connection', function (socket) {
        console.log('A connection has arrived!');
        
        /* Variable to record radar data */
        var radar_data = [];

        //var server = net.createServer(function(c) { 
            //console.log('client connected');
            //c.on('end', function() {
                //console.log('client disconnected');
            //});

            //c.on('data', function(data) {

                //// Avoid out of memory errors by trimming 
                //// the radar_data if more than 1000 values get accumulated
                //if(radar_data.length > 1000) {
                    //radar_data.splice(0);
                //}

                //radar_data.push(data.toString('utf8'));
                //socket.emit('radardata', {
                    //data:data.toString('utf8')
                //});
            //});
        //});
        //server.listen(8124, function() {
            //console.log("Radar data server listening on 8124"); 
        //});

        socket.on('disconnect', function(){
            console.log('user disconnected');
            server.close(function() {
                console.log("Server closing");    
            });
        });
        
        socket.on('recognize', function (skeleton_data, fn) {

            // To remove excessive elements in the buffer
            // Expecting the radar sampling rate at a max of 250
            if(radar_data.length > 250) {
                radar_data.splice(0);
                return;
            }

            var actions = ActivityRecognizer.run(skeleton_data);
            recordActions(skeleton_data, radar_data, actions);
            //console.log(radar_data.length);
            radar_data.splice(0);
            fn(actions);
        });
    });

    function recordActions(skeleton_data, radar_data, actions) {
        var radar_vps = radar_data.length;
        var recorded_data = { 
            "skeleton_data":skeleton_data,
            "radar_data":radar_data,
            "actions":actions,
            "timestamp":Date.now()
        };

        var recorded_data_str = JSON.stringify(recorded_data);
        recorded_data_str = "\n" + recorded_data_str;
        //console.log(recorded_data_str);

        fs.appendFile('recorded_data/log.txt', recorded_data_str, function (err) {
            if (err) throw err;
            console.log(Date.now() + ': Data recorded in file. Radar values recorded: ' + radar_vps );
        });


    }
};


module.exports = SocketModel;

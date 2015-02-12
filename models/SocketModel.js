var io,
    self,
    ActivityRecognizer = require('./ActivityRecognizer');
    var net = require('net');


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

        var server = net.createServer(function(c) { 
            console.log('client connected');
            c.on('end', function() {
                console.log('client disconnected');
            });

            c.on('data', function(data) {
                console.log(data.toString('utf8'));   
                socket.emit('radardata', {
                    data:data.toString('utf8')
                });
            });
        });
        server.listen(8124, function() {
            console.log("Radar data server listening on 8124"); 
        });

        socket.on('disconnect', function(){
            console.log('user disconnected');
            server.close(function() {
                console.log("Server closing");    
            });
        });
        
        //socket.on('getRadarData', function(){
            //console.log('getRadarData()');
            //socket.emit('recordRadarData', {
                //data:"some random data"    
            //});
        //});

        socket.on('recognize', function (data, fn) {
            var actions = ActivityRecognizer.run(data);
            recordActions(data, actions);
            fn(actions);
        });
    });

    function recordActions(data, actions) {
        console.log(data, actions);    
    }
};


module.exports = SocketModel;

var port = 7000;
var io = require('socket.io').listen(port, {log: false});

console.log('Server Running...');
console.log('Port: ' + port);

io.sockets.on('connection', function(socket){
	socket.on('update', function(data){
		console.log('update recived');
		io.sockets.emit('update-chart', {});
	});
});
$(document).ready(function(){
    var socket = io.connect();

    socket.on('connect', function() {
        console.log('Connected!');
    });
    socket.on('disconnect', function() {
        console.log('Disconnected!');
    });
    socket.on('game_update', function(msg) {
        const ctx = document.getElementById('game-canvas').getContext('2d');
        ctx.clearRect(0, 0, 600, 600);

        ctx.font = "20px Arial";
        ctx.fillStyle = "#000000";

        game_update = JSON.parse(msg.data);
        console.log(game_update);

        for (let i = 0; i < game_update.tanks.length; i++) {
            tank = game_update.tanks[i];

            tank_text = "";
            if (tank.direction == "UP") {
                tank_text = "^T";
            } else if (tank.direction == "DOWN") {
                tank_text = "vT";
            } else if (tank.direction == "LEFT") {
                tank_text = "<T";
            } else if (tank.direction == "RIGHT") {
                tank_text = ">T";
            }

            ctx.fillText(tank_text, tank.x * 4, tank.y * 4);
        }

        for (let i = 0; i < game_update.bullets.length; i++) {
            bullet = game_update.bullets[i];

            bullet_text = "";
            if (bullet.direction == "UP") {
                bullet_text = "^B";
            } else if (bullet.direction == "DOWN") {
                bullet_text = "vB";
            } else if (bullet.direction == "LEFT") {
                bullet_text = "<B";
            } else if (bullet.direction == "RIGHT") {
                bullet_text = ">B";
            }

            ctx.fillText(bullet_text, bullet.x * 4, bullet.y * 4);
        }
    });

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    // $('form#emit').submit(function(event) {
    //     socket.emit('my_event', {data: $('#emit_data').val()});
    //     return false;
    // });
    // $('form#broadcast').submit(function(event) {
    //     socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
    //     return false;
    // });
    // $('form#join').submit(function(event) {
    //     socket.emit('join', {room: $('#join_room').val()});
    //     return false;
    // });
    // $('form#leave').submit(function(event) {
    //     socket.emit('leave', {room: $('#leave_room').val()});
    //     return false;
    // });
    // $('form#send_room').submit(function(event) {
    //     socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
    //     return false;
    // });
    // $('form#close').submit(function(event) {
    //     socket.emit('close_room', {room: $('#close_room').val()});
    //     return false;
    // });
    // $('form#disconnect').submit(function(event) {
    //     socket.emit('disconnect_request');
    //     return false;
    // });
});

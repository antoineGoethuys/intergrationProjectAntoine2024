<?php
/*
Plugin Name: RabbitMQ Data Gatherer
Description: A plugin to gather data from RabbitMQ.
Version: 1.0
Author: Your Name
*/

// Include the php-amqplib library
require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

function connect_to_rabbitmq() {
    // RabbitMQ server details
    $host = 'localhost';
    $port = 3300;
    $user = 'guest';
    $password = 'guest';
    $queue = 'your_queue_name';

    // Establish connection
    $connection = new AMQPStreamConnection($host, $port, $user, $password);
    $channel = $connection->channel();

    // Declare the queue
    $channel->queue_declare($queue, false, true, false, false);

    // Callback function to process messages
    $callback = function($msg) {
        // Process the message
        error_log('Received: ' . $msg->body);
    };

    // Consume messages
    $channel->basic_consume($queue, '', false, true, false, false, $callback);

    // Wait for incoming messages
    while($channel->is_consuming()) {
        $channel->wait();
    }

    // Close the channel and connection
    $channel->close();
    $connection->close();
}

// Hook the function to WordPress init action
add_action('init', 'connect_to_rabbitmq');
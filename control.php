<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
header("Content-Type: text/plain; charset=UTF-8");

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "smart_agriculture"; 

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Database Connection Failed: " . $conn->connect_error);
}

if (isset($_GET['device']) && isset($_GET['action'])) {
    $device = $conn->real_escape_string($_GET['device']);   
    $action = (int)$_GET['action'];   

    $sql = "UPDATE device_status SET status = $action WHERE device_name = '$device'";
    
    if ($conn->query($sql) === TRUE) {
        echo "Successfully updated $device to $action";
    } else {
        echo "Error updating record: " . $conn->error;
    }
}
$conn->close();
?>
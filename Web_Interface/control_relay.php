<?php

     $relay_id = $_GET["relay_id"];
     $relay_pin = $_GET["relay_pin"];
     $status = $_GET["status"];

     // Include database connection
     include "database_connection.php";

     // Connect to the database
     $conn = OpenDatabase();

     $sql = "UPDATE relay_pins SET status = '$status' WHERE relay_id = $relay_id and relay_pin = $relay_pin";
     $result = $conn->query($sql);

     $conn->close();

?>

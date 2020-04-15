<?php

     $gpio_pin = $_GET["gpio_pin"];
     
     // Include database connection
     include "database_connection.php";

     // Connect to the database
     $conn = OpenDatabase();

     $sql = "SELECT status from sensors where gpio_pin = $gpio_pin";
     $result = $conn->query($sql);

     if ($result->num_rows > 0) {
          // output data of each row
          while($row = $result->fetch_assoc()) {
               echo $row["status"];
          }
     } else {
          echo "N/A";
     }

     $conn->close();

?>

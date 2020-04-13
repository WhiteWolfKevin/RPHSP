<?php

     $gpio_pin = $_GET["gpio_pin"];

     $servername = "piserver.lan";
     $username = "rphsp";
     $password = "password";
     $database = "rphsp";

     // Create connection
     $conn = new mysqli($servername, $username, $password, $database);

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

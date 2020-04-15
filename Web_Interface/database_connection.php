<?php

     function OpenDatabase() {
          // Set the variables for the database connection
          $servername = "piserver.lan";
          $username = "rphsp";
          $password = "password";
          $database = "rphsp";

          // Create connection
          $conn = new mysqli($servername, $username, $password, $database);

          return $conn;
     }

     function CloseDatabase($conn) {
          $conn->close();
     }

?>

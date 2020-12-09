<?php

     // Get the possible variables that are sent in
     $pin_code = $_GET["pin_code"];

     # Contine if the pin_code is set
     if (isset($pin_code)) {

          // Include database connection
          include "database_connection.php";

          // Connect to the database
          $conn = OpenDatabase();

          // Get all of the pin codes from the database
          $sql = "SELECT pin_code from pin_codes";
          $result = $conn->query($sql);

          if ($result->num_rows > 0) {
               // Run through each result from the database
               while($row = $result->fetch_assoc()) {
                    if ($row["pin_code"] == $pin_code) {
                         echo "Access Granted";
                         exit();
                    }
               }
               echo "Access Denied";
          } else {
               echo "Access Denied";
          }
     } else {
          echo "ERROR - WEB";
     }

     CloseDatabase($conn);
?>

<?php

     // Get the possible variables that are sent in
     $pin_code = $_GET["pin_code"];
     $rfid_card_number = $_GET["rfid_card_number"];

     # Contine if one of the items is set
     if (isset($pin_code) || isset($rfid_card_number)) {

          // Include database connection
          include "database_connection.php";

          // Connect to the database
          $conn = OpenDatabase();

          // Determine which authentication item is set and proceed accordingly
          if (isset($pin_code)) {

               // Get all of the pin codes from the database
               $sql = "SELECT pin_code from pin_codes";
               $result = $conn->query($sql);

               if ($result->num_rows > 0) {
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                         if ($row["pin_code"] == $pin_code) {
                              echo "Access Granted";

                              // Disconnect from the database
                              CloseDatabase($conn);

                              exit();
                         }
                    }
                    echo "Access Denied";
               }
          } else {

               // Get all of the card numbers from the database
               $sql = "SELECT card_number from rfid_cards";
               $result = $conn->query($sql);

               if ($result->num_rows > 0) {
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                         if ($row["card_number"] == $rfid_card_number) {
                              echo "Access Granted";

                              // Disconnect from the database
                              CloseDatabase($conn);

                              exit();
                         }
                    }
                    echo "Access Denied";
               }
          }

          // Disconnect from the database
          CloseDatabase($conn);

     } else {
          echo "Access Denied";
     }

?>

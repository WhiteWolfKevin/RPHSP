<?php

     // Get the possible variables that are sent in
     $pin_code = $_GET["pin_code"];
     $rfid_card_number = $_GET["rfid_card_number"];

     $log_file = fopen('log.txt', 'w') or die("Unable to open file!");
     // Write to the log file
     fwrite($log_file, date('Y-m-d H:i:s') . " : Pin $pin_code entered\n");
     fwrite($log_file, date('Y-m-d H:i:s') . " : RFID $rfid_card_number entered\n");
     fclose($log_file);

     # Contine if one of the items is set
     if (isset($pin_code) || isset($rfid_card_number)) {

          // Include database connection
          include "database_connection.php";

          // Connect to the database
          $conn = OpenDatabase();

          # Contine if the pin_code is set
          if (isset($pin_code)) {
               // Get all of the pin codes from the database
               $sql = "SELECT pin_code from pin_codes";
               $result = $conn->query($sql);

               if ($result->num_rows > 0) {
                    // Run through each result from the database
                    while($row = $result->fetch_assoc()) {
                         if ($row["pin_code"] == $pin_code) {
                              echo "Access Granted";
                              exit();
                         } else {
                              echo "Access Denied";
                         }
                    }
               } else {
                    echo "Access Denied";
               }
          } else if(isset($rfid_card_number)) {
               // Get all of the card numbers from the database
               $sql = "SELECT card_number from rfid_cards";
               $result = $conn->query($sql);

               if ($result->num_rows > 0) {
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                         if ($row["card_number"] == $rfid_card_number) {
                              echo "Access Granted";
                              exit();
                         } else {
                              echo "Access Denied";
                         }
                    }
               }
          } else {
               echo "ERROR - WEB";
          }
     }
     CloseDatabase($conn);
?>

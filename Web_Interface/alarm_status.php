<?php

     // Include database connection
     include "database_connection.php";

     // Connect to the database
     $conn = OpenDatabase();

     // Get all of the pin codes from the database
     $sql = "SELECT status from alarms where id = 1";
     $result = $conn->query($sql);

     if ($result->num_rows > 0) {
          // Output result
          $row = $result->fetch_assoc();
          echo $row["status"];
     } else {
          echo "ERROR - WEB";
     }
     // Disconnect from the database
     CloseDatabase($conn);

?>

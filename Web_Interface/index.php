<!DOCTYPE html>
<html>
<head>
     <style>
     #statusBoxClosed {
          background-color: #cfc ;
          display: inline-block;
     }
     #statusBoxOpen {
          background-color: #ff0000 ;
          display: inline-block;
     }
     #statusBoxUnknown {
          background-color: #ff8000 ;
          display: inline-block;
     }
     </style>
</head>

<body>

     <h1>Raspberry Pi Home Security System</h1>

     <?php

     // Include database connection
     include "database_connection.php";

     // Connect to the database
     $conn = OpenDatabase();

     $sql = "SELECT * from sensors";
     $result = $conn->query($sql);

     // Array holding all sensors gpios for javascript
     $sensors = [];

     if ($result->num_rows > 0) {
          // Display each field
          while($row = $result->fetch_assoc()) {
               echo "Name: " . $row["name"] . "<br>";
               echo "Type: " . $row["type"] . "<br>";
               echo "GPIO Pin: " . $row["gpio_pin"] . "<br>";
               echo "Status: ";
               echo "<div style='display: inline-block;' id='gpio_pin_" . $row["gpio_pin"] . "'></div>";

               echo "<br>";
               echo "<br>";

               // Add each gpio_pin to the array for the javascript
               array_push($sensors, $row["gpio_pin"]);

          }
     } else {
          echo "0 results";
     }

     $conn->close();
     ?>



     <script>

          var sensors = <?php echo json_encode($sensors); ?>

          function loadSensorStatus(sensors_array) {
               setInterval(function(){
                    sensors_array.forEach(getSensorStatus)
               }
               , 1000);
          }

          function getSensorStatus(gpio_pin) {
               var xhttp = new XMLHttpRequest();
               xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                         if (this.responseText == "OPEN") {
                              document.getElementById("gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxOpen'>" + this.responseText + "</div>";
                         } else if (this.responseText == "CLOSED") {
                              document.getElementById("gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxClosed'>" + this.responseText + "</div>";
                         } else {
                              document.getElementById("gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxUnknown'>" + this.responseText + "</div>";
                         }
                    }
               };
               xhttp.open("GET", "data.php?gpio_pin=" + gpio_pin, true);
               xhttp.send();
          }

          loadSensorStatus(sensors);

     </script>
</body>
</html>

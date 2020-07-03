<!DOCTYPE html>
<html>
<head>
     <style>
     /* Styling for sensor status */
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

     /* Styling for relay status */
     #relayChannelOn {
          background-color: #cfc ;
          display: inline-block;
     }
     #relayChannelOff {
          background-color: #ff0000 ;
          display: inline-block;
     }
     #relayChannelUnknown {
          background-color: #ff8000 ;
          display: inline-block;
     }


     table, th, td {
          border: 1px solid black;
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

     echo "<table>";

     if ($result->num_rows > 0) {
          // Display each field
          while($row = $result->fetch_assoc()) {
               echo "<tr>";
                    echo "<td><b>Name: </b></td><td>" . $row["name"] . "</td>";
               echo "</tr>";

               echo "<tr>";
                    echo "<td><b>Type: </b></td><td>" . $row["type"] . "</td>";
               echo "</tr>";

               echo "<tr>";
                    echo "<td><b>GPIO Pin: </b></td><td>" . $row["gpio_pin"] . "</td>";
               echo "</tr>";

               echo "<tr>";
                    echo "<td><b>Status: </b></td><td><div style='display: inline-block;' id='sensor_div_id_gpio_pin_" . $row["gpio_pin"] . "'></div></td>";
               echo "</tr>";

               echo "<tr>";
                    echo "<td><br /></td>";
               echo "</tr>";

               // Add each gpio_pin to the array for the javascript
               array_push($sensors, $row["gpio_pin"]);

          }
     } else {
          echo "0 results";
     }

     echo "</table>";
     echo "</br></br>";

     // Starting dynamic entry of relays into web interace 20200702 - This section will eventually replace above static relay test
     $sql = "SELECT * from relays";
     $relaysResult = $conn->query($sql);

     echo "<table>";

     if ($relaysResult->num_rows > 0) {
          // Display each field
          while($row = $relaysResult->fetch_assoc()) {
               echo "<tr>";
                    echo "<td><b>Name: </b></td><td>" . $row["relay_name"] . "</td>";
               echo "</tr>";

               echo "<tr>";
                    echo "<td><b>Channels: </b></td><td>" . $row["channels"] . "</td>";
               echo "</tr>";

               $sql = "SELECT * from relay_pins where relay_id = " . $row["relay_id"];
               $relayPinsResult = $conn->query($sql);

                    if ($relayPinsResult->num_rows > 0) {
                         // Display each field
                         while($innerRow = $relayPinsResult->fetch_assoc()) {
                              echo "<tr>";
                                   echo "<td><b>Pin: </b></td><td>" . $innerRow["relay_pin"] . "</td>";
                                   echo "<td><b>Status: </b></td><td><div style='display: inline-block;' id='relay_div_id_gpio_pin_" . $innerRow["relay_pin"] . "'></div></td>";
                                   echo "<td><button type='button' onclick='relayOn(" . $row["relay_id"] . ", " . $innerRow["relay_pin"] . ")'>On</button></td>";
                                   echo "<td><button type='button' onclick='relayOff(" . $row["relay_id"] . ", " . $innerRow["relay_pin"] . ")'>Off</button></td>";
                              echo "</tr>";
                         }
                    } else {
                         echo "0 results";
                    }


               echo "<tr>";
                    echo "<td><br /></td>";
               echo "</tr>";

          }
     } else {
          echo "0 results";
     }



     echo "</table>";







     $conn->close();
     ?>
     <script>

          // Javascript for the live view of sensors

          // Grab the sensors array from PHP
          var sensors = <?php echo json_encode($sensors); ?>

          // Function for live updating sensor status
          function loadSensorStatus(sensors_array) {
               setInterval(function(){
                    sensors_array.forEach(getSensorStatus)
               }
               , 1000);
          }

          // Function to get sensor status and display it
          function getSensorStatus(gpio_pin) {
               var xhttp = new XMLHttpRequest();
               xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                         if (this.responseText == "OPEN") {
                              document.getElementById("sensor_div_id_gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxOpen'>" + this.responseText + "</div>";
                         } else if (this.responseText == "CLOSED") {
                              document.getElementById("sensor_div_id_gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxClosed'>" + this.responseText + "</div>";
                         } else {
                              document.getElementById("sensor_div_id_gpio_pin_" + gpio_pin).innerHTML = "<div id='statusBoxUnknown'>" + this.responseText + "</div>";
                         }
                    }
               };
               xhttp.open("GET", "data.php?gpio_pin=" + gpio_pin, true);
               xhttp.send();
          }

          // Function to start liveview of sensor status
          loadSensorStatus(sensors);

          // Javascript for the control of the relay boards
          function relayOn(relay_id, relay_pin) {
               var xhttp = new XMLHttpRequest();
               xhttp.open("GET", "control_relay.php?relay_id=" + relay_id + "&relay_pin=" + relay_pin + "&status=ON", true);
               xhttp.send();
          }

          function relayOff(relay_id, relay_pin) {
               var xhttp = new XMLHttpRequest();
               xhttp.open("GET", "control_relay.php?relay_id=" + relay_id + "&relay_pin=" + relay_pin + "&status=OFF", true);
               xhttp.send();
          }





     </script>
</body>
</html>

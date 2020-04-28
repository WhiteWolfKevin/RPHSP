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
                    echo "<td><b>Status: </b></td><td><div style='display: inline-block;' id='gpio_pin_" . $row["gpio_pin"] . "'></div></td>";
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





     // Stuff for relay control
     ?>
     <br><br>
     <table>
          <tr>
               <td>
                    Relay 1
               </td>
               <td>
                    <button type="button" onclick="relayOn(1, 4)">On</button>
               </td>
               <td>
                    <button type="button" onclick="relayOff(1, 4)">Off</button>
               </td>
          </tr>
          <tr>
               <td>
                    Relay 2
               </td>
               <td>
                    <button type="button" onclick="relayOn(1, 17)">On</button>
               </td>
               <td>
                    <button type="button" onclick="relayOff(1, 17)">Off</button>
               </td>
          </tr>
          <tr>
               <td>
                    Relay 3
               </td>
               <td>
                    <button type="button" onclick="relayOn(1, 27)">On</button>
               </td>
               <td>
                    <button type="button" onclick="relayOff(1, 27)">Off</button>
               </td>
          </tr>
          <tr>
               <td>
                    Relay 4
               </td>
               <td>
                    <button type="button" onclick="relayOn(1, 22)">On</button>
               </td>
               <td>
                    <button type="button" onclick="relayOff(1, 22)">Off</button>
               </td>
          </tr>
     </table>
     <?php
















     $conn->close();
     ?>
     <script>

          // Javascript for the live view of sensors
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





          // Javascript for the control of the relay board
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

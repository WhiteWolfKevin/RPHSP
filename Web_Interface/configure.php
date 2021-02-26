<!DOCTYPE html>
<html>
<head>
     <style>

     </style>
</head>

<body>

     <h1>Configure - Raspberry Pi Home Security System</h1>

     <form action="index.php">
          <button type"submit">RPHSP Home</button>
     </form>

     <hr>
     <h3>Add New User</h3>
     <hr>
     <form>
          <label for="firstName">First Name:</label><br>
          <input type="text" id="firstName" name="firstName"><br><br>

          <label for="lastName">Last Name:</label><br>
          <input type="text" id="lastName" name="lastName"><br><br>

          <label for="userEnabled">User Enabled:</label><br>
          <input type="checkbox" id="userEnabled" name="userEnabled" value="Enabled"><br><br>

          <label for="pinCode">Pin Code:</label><br>
          <input type="text" id="pinCode" name="pinCode"><br><br>

          <label for="rfidHexCode">RFID Hex Code:</label><br>
          <input type="text" id="rfidHexCode" name="rfidHexCode"><br><br>
     </form>

     <br>

     <hr>
     <h3>Add New Sensor</h3>
     <hr>
     <form>
          <label for="sensorGPIO">Select GPIO Pin for Sensor (BCM Mode)</label>
          <select name="sensorGPIO" id="sensorGPIO">
               <?php
                    for($i = 0; $i <= 28; $i++) {
                         ?>
                              <option value="<?php echo $i;?>"><?php echo $i;?></option>
                         <?php
                    }
               ?>

          </select><br><br>

          <label for="sensorName">Sensor Name:</label><br>
          <input type="text" id="sensorName" name="sensorName"><br><br>

          <label for="sensorType">Sensor Type:</label><br>
          <input type="text" id="sensorType" name="sensorType"><br><br>
     </form>

</body>

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

<script type="text/javascript">
  function loadDoc() {
    setInterval(function(){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         document.getElementById("liveUpdate").innerHTML = this.responseText;
        }
      };
      xhttp.open("GET", "data.php", true);
      xhttp.send();
    },1000);
  }
  loaddoc();
</script>

</head>
<body>

<h1>Raspberry Pi Home Security System</h1>

<?php

  ?>
  <h1><class="testliveupdate" id="liveUpdate">5</h1>
  <?php



  $servername = "piserver.lan";
  $username = "rphsp";
  $password = "password";
  $database = "rphsp";

  // Create connection
  $conn = new mysqli($servername, $username, $password, $database);

  $sql = "SELECT * from sensors";
  $result = $conn->query($sql);

  if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
      echo "Name: " . $row["name"] . "<br>";
      echo "Type: " . $row["type"] . "<br>";
      echo "GPIO Pin: " . $row["gpio_pin"] . "<br>";
      echo "Status: ";

      ?>
      <class="testliveupdate" id="liveUpdate">
      <?php

      // if($row["status"] == "CLOSED") {
      //   echo "<div id='statusBoxClosed'>" . $row["status"] . "</div>";
      // } else if ($row["status"] == "OPEN") {
      //   echo "<div id='statusBoxOpen'>" . $row["status"] . "</div>";
      // } else {
      //   echo "<div id='statusBoxUnknown'>" . $row["status"] . "</div>";
      // }

      echo "<br>";
      echo "<br>";
    }
  } else {
      echo "0 results";
  }

  $conn->close();
?>

</body>
</html>

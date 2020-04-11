<!DOCTYPE html>
<html>
<head>
<style>
#statusBoxClosed {
  background-color: #cfc ;
}
#statusBoxOpen {
  background-color: #ff0000 ;
}
</style>
</head>
<body>

<h1>Raspberry Pi Home Security System</h1>

<?php

  $redis = new Redis();
  //Connecting to Redis
  $redis->connect('piserver', 6379);

  echo "<h2>Alarm Status: " . $redis->get("alarmStatus") . "</h2>";

  echo "Statically Created Content";
  echo "<br>";

  if($redis->get("Basement Door") == "CLOSED") {
    echo "Basement Door: " . "<div id='statusBoxClosed'>" . $redis->get("Basement Door") . "</div>";
    echo "<br>";
  } else if ($redis->get("Basement Door") == "OPEN - WARNING!!!") {
    echo "Basement Door: " . "<div id='statusBoxOpen'>" . $redis->get("Basement Door") . "</div>";
    echo "<br>";
  }

  if($redis->get("Front Door") == "CLOSED") {
    echo "Front Door: " . "<div id='statusBoxClosed'>" . $redis->get("Front Door") . "</div>";
    echo "<br>";
  } else if ($redis->get("Front Door") == "OPEN - WARNING!!!") {
    echo "Front Door: " . "<div id='statusBoxOpen'>" . $redis->get("Front Door") . "</div>";
    echo "<br>";
  }

  if($redis->get("Garage Door") == "CLOSED") {
    echo "Garage Door: " . "<div id='statusBoxClosed'>" . $redis->get("Garage Door") . "</div>";
    echo "<br>";
  } else if ($redis->get("Garage Door") == "OPEN - WARNING!!!") {
    echo "Garage Door: " . "<div id='statusBoxOpen'>" . $redis->get("Garage Door") . "</div>";
    echo "<br>";
  }

  if($redis->get("Living Room Window") == "CLOSED") {
    echo "Living Room Window: " . "<div id='statusBoxClosed'>" . $redis->get("Living Room Window") . "</div>";
    echo "<br>";
  } else if ($redis->get("Living Room Window") == "OPEN - WARNING!!!") {
    echo "Living Room Window: " . "<div id='statusBoxOpen'>" . $redis->get("Living Room Window") . "</div>";
    echo "<br>";
  }


  echo "Content from MariaDB";
  echo "<br>";

  $servername = "piserver.lan";
  $username = "rphsp";
  $database = "rphsp";

  // Create connection
  //$conn = new mysqli($servername, $username);
  $conn = new mysqli($servername, $username, $database);

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  }
  echo "Connected successfully";
  echo "<br>";

  $sql = "SELECT * from sensors";
  $result = $conn->query($sql);

  if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
      echo "Name: " . $row["name"] . "<br>";
      echo "Type: " . $row["type"] . "<br>";
      echo "GPIO Pin: " . $row["gpio_pin"] . "<br>";
      echo "Status: " . $row["status"] . "<br>";
      echo "<br>";
    }
  } else {
      echo "0 results";
  }






  $conn->close();
?>

</body>
</html>

<?php
$conn = mysqli_connect("localhost", "root", "", "college");


    $id = $_GET['id'];
    $sql = "DELETE  FROM faculty WHERE Faculty_ID ='".$id."'";
    
    if ($conn->query($sql) === TRUE) {
        header("Location: facultyrecord.php");
        
    } else {
        echo "Error deleting record: " . $conn->error;
    }
    $conn->close();

?>

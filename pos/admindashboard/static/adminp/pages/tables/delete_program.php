<?php
$conn = mysqli_connect("localhost", "root", "", "college");


    $id = $_GET['id'];
    $sql = "DELETE  FROM program WHERE id ='".$id."'";
    
    if ($conn->query($sql) === TRUE) {
        header("Location: mprogram.php");
        
    } else {
        echo "Error deleting record: " . $conn->error;
    }
    $conn->close();

?>

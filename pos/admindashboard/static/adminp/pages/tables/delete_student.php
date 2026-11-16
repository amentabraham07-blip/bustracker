<?php
$conn = mysqli_connect("localhost", "root", "", "college");


    $id = $_GET['id'];
    $sql = "DELETE  FROM student WHERE Admission_NO ='".$id."'";
    
    if ($conn->query($sql) === TRUE) {
        header("Location: studentrecord.php");
        
    } else {
        echo "Error deleting record: " . $conn->error;
    }
    $conn->close();

?>

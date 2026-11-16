<?php
$conn = mysqli_connect("localhost", "root", "", "college");


    $id = $_GET['id'];
    $sql = "DELETE  FROM department WHERE id ='".$id."'";
    
    if ($conn->query($sql) === TRUE) {
        header("Location: mdepartment.php");
        
    } else {
        echo "Error deleting record: " . $conn->error;
    }
    $conn->close();

?>

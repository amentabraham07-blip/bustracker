<?php
$conn = mysqli_connect("localhost", "root", "", "college");

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $id = $_POST['Department_ID'];
    $name = $_POST['Department_Name'];
    $moto = $_POST['Department_Moto'];

    // Prepare SQL update query
    $sql = "UPDATE department SET 
            Department_Name = COALESCE(NULLIF('$name', ''), Department_Name),
            Department_Moto = COALESCE(NULLIF('$moto', ''), Department_Moto)
            WHERE Department_ID = $id";
    
    if ($conn->query($sql) === TRUE) {
        echo "Record updated successfully";
    } else {
        echo "Error updating record: " . $conn->error;
    }
    $conn->close();
}
?>

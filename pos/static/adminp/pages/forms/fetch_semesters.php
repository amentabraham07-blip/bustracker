<?php
include 'db_connection.php'; // Include your database connection

if (isset($_GET['program'])) {
    $program = $_GET['program'];
    $sql = "SELECT No_Of_Semester FROM program WHERE Program_Name = '$program'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $semesters = $row['No_Of_Semester'];
        echo "<option value=''>Select Semester</option>";
        for ($i = 1; $i <= $semesters; $i++) {
            echo "<option value='$i'>Semester $i</option>";
        }
    } else {
        echo "<option value=''>No Semesters Found</option>";
    }
}
?>

<?php
$conn = mysqli_connect("localhost", "root", "", "college");

if (isset($_POST['Program_Name'])) {
    $Program_Name = $_POST['Program_Name'];
    $query = "SELECT No_Of_Semester FROM program WHERE Program_Name = '$Program_Name'";
    $result = mysqli_query($conn, $query);

    echo "<option value=''>Select Semester</option>"; // Default option

    if ($row = mysqli_fetch_assoc($result)) {
        $no_of_semesters = $row['No_Of_Semester'];

        // Generate semester options from 1 to No_Of_Semester
        for ($i = 1; $i <= $no_of_semesters; $i++) {
            echo "<option value='$i'>$i</option>";
        }
    }
}
?>

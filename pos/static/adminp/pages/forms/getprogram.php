<?php
$conn = mysqli_connect("localhost", "root", "", "college");

if (isset($_POST['Department_Name'])) {
	$department = $_POST['Department_Name'];
	$query = "SELECT Program_Name FROM program WHERE Department_Name = '$department'";
	$result = mysqli_query($conn, $query);
	
	echo "<option value=''>Select Program</option>";
	while ($row = mysqli_fetch_assoc($result)) {
		echo "<option value='" . $row['Program_Name'] . "'>" . $row['Program_Name'] . "</option>";
	}
}
?>

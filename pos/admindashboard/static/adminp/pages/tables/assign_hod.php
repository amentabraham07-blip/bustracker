<?php
$conn = mysqli_connect("localhost", "root", "", "college");

if (isset($_POST['facultyID']) && isset($_POST['department'])) {
    $facultyID = $_POST['facultyID'];
    $department = $_POST['department'];

    // Revert any existing HOD in the same department
    $sql = "UPDATE faculty SET Rights = 'Faculty' WHERE Department_Name = ? AND Rights = 'HOD'";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param('s', $department);
    $stmt->execute();

    // Assign the HOD role to the selected faculty
    $sql = "UPDATE faculty SET Rights = 'HOD' WHERE Faculty_ID = ? AND Department_Name = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param('is', $facultyID, $department);
    $stmt->execute();

    // Check if Faculty_ID is in classincharge table, and remove it if present
    $sql = "UPDATE classincharge SET Faculty_ID = NULL WHERE Faculty_ID = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param('i', $facultyID);
    $stmt->execute();

    echo "HOD Assigned Successfully and Faculty ID removed from Class Incharge table if present.";
} else {
    echo "Invalid request.";
}
?>

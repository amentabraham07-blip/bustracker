<?php
// approvefaculty.php
if (isset($_GET['id'])) {
    // Get the faculty ID from the URL
    $facultyID = $_GET['id'];

    // Database connection
    $conn = mysqli_connect("localhost", "root", "", "college");

    // Update query to approve the faculty
    $sql = "UPDATE faculty SET Rights = 'faculty' WHERE Faculty_ID = '$facultyID'";

    if (mysqli_query($conn, $sql)) {
        echo "<script>
                alert('Faculty approved successfully!');
                window.location.href = 'facultyapproval.php'; // Redirect back to the list
              </script>";
    } else {
        echo "<script>alert('Error approving faculty!');</script>";
    }

    // Close connection
    mysqli_close($conn);
}
?>

<?php
// Connect to the database
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if 'id' parameter is set and valid
if (isset($_GET['id']) && !empty($_GET['id'])) {
    $course_id = $_GET['id'];  // Get the Course_Code from the URL

    // Prepare the DELETE query
    $sql = "DELETE FROM course WHERE Course_Code = ?";
    
    // Check if the query was prepared successfully
    if ($stmt = $conn->prepare($sql)) {
        $stmt->bind_param("s", $course_id);  // Bind the course_code as a string parameter

        // Execute the query
        if ($stmt->execute()) {
            // Redirect back to the course management page with a success message
            header("Location: mcourse.php?status=deleted");
            exit();
        } else {
            // Show an error message if the deletion failed
            echo "<script>alert('Error deleting course');</script>";
        }

        // Close the statement
        $stmt->close();
    } else {
        // Show an error if the prepared statement failed
        echo "<script>alert('Error preparing query');</script>";
    }
} else {
    // If course_id is not set or empty, show an error
    echo "<script>alert('Invalid course ID');</script>";
}

// Close the database connection
$conn->close();
?>

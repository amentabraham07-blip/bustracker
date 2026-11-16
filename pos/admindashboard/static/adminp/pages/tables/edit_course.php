<?php
// Database connection
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if ID is set
if (isset($_GET['id']) && !empty($_GET['id'])) {
    $course_code = $_GET['id'];

    // Fetch the current course details from the database
    $sql = "SELECT * FROM course WHERE Course_Code = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $course_code);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $program_name = $row['Program_Name'];
        $course_code = $row['Course_Code'];
        $course_name = $row['Course_Name'];
        $duration = $row['Duration'];
    } else {
        // Redirect if course is not found
        header("Location: mcourse.php?error=notfound");
        exit;
    }

    $stmt->close();
} else {
    // Redirect if ID is not valid
    header("Location: mcourse.php");
    exit;
}

// Handle form submission for updating course
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $new_program_name = $_POST['program_name'];
    $new_course_code = $_POST['course_code'];
    $new_course_name = $_POST['course_name'];
    $new_duration = $_POST['duration'];

    // Check if the Course_Code already exists (except for the current course)
    $sql = "SELECT * FROM course WHERE Course_Code = ? AND Course_Code != ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $new_course_code, $course_code); // Use "ss" for two string parameters
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        echo "<script>alert('Error: The Course Code already exists.');</script>";
    } else {
        // Update the course record
        $stmt = $conn->prepare("UPDATE course SET Program_Name = ?, Course_Name = ?, Duration = ? WHERE Course_Code = ?");
        $stmt->bind_param("ssss", $new_program_name, $new_course_name, $new_duration, $course_code);

        if ($stmt->execute()) {
            // Redirect after success
            header("Location: mcourse.php?status=updated");
        } else {
            echo "<script>alert('Error updating course: " . $stmt->error . "');</script>";
        }
        $stmt->close();
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Edit Course</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css">
</head>
<?php
// Database connection
$conn = mysqli_connect("localhost", "root", "", "college");
?>

<body class="skin-blue">
    <div class="wrapper">
        <!-- Main Header -->
        <header class="main-header">
            <a href="../../index2.html" class="logo"><b>MES</b>College</a>
            <nav class="navbar navbar-static-top" role="navigation">
                <div class="navbar-custom-menu">
                    <ul class="nav navbar-nav">
                        <li class="dropdown user user-menu">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                <img src="../../dist/img/user2-160x160.jpg" class="user-image" alt="User Image"/>
                                <span class="hidden-xs"><b>Admin@MESErumely</b></span>
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </header>

        <!-- Content Wrapper -->
        <div class="content-wrapper">
            <section class="content-header">
                <h1>
                    <b>Edit Course</b>
                </h1>
                <ol class="breadcrumb">
                    <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
                    <li><a href="#">Manage Courses</a></li>
                    <li><a href="#">Edit Course</a></li>
                </ol>
            </section>

            <!-- Main content -->
            <section class="content">
                <div class="row">
                    <div class="col-xs-12">
                        <div class="box">
                            <div class="box-header">
                                <h3 class="box-title">Edit Course Information</h3>
                            </div>

                            <div class="box-body">
                                <form action="edit_course.php?id=<?php echo htmlspecialchars($course_code); ?>" method="POST">
                                    <!-- Program Name Dropdown -->
                                    <div class="form-group">
                                        <label for="program_name">Program Name</label>
                                        <select class="form-control" id="program_name" name="program_name" required>
                                            <?php
                                            // Fetch all programs for the dropdown
                                            $sql = "SELECT Program_Name FROM program";
                                            $result = $conn->query($sql);
                                            while ($program = $result->fetch_assoc()) {
                                                echo "<option value='" . htmlspecialchars($program['Program_Name']) . "'";
                                                if ($program['Program_Name'] == $program_name) {
                                                    echo " selected";
                                                }
                                                echo ">" . htmlspecialchars($program['Program_Name']) . "</option>";
                                            }
                                            ?>
                                        </select>
                                    </div>

                                    <!-- Course Code (Text Input) -->
                                    <div class="form-group">
                                        <label for="course_code">Course Code</label>
                                        <input type="text" class="form-control" id="course_code" name="course_code" value="<?php echo htmlspecialchars($course_code); ?>" required>
                                    </div>

                                    <!-- Course Name -->
                                    <div class="form-group">
                                        <label for="course_name">Course Name</label>
                                        <input type="text" class="form-control" id="course_name" name="course_name" value="<?php echo htmlspecialchars($course_name); ?>" required>
                                    </div>

                                    <!-- Duration -->
                                    <div class="form-group">
                                        <label for="duration">Duration</label>
                                        <input type="text" class="form-control" id="duration" name="duration" value="<?php echo htmlspecialchars($duration); ?>" required>
                                    </div>

                                    <!-- Submit Button -->
                                    <button type="submit" class="btn btn-success">Save Changes</button>
                                    <a href="mcourse.php" class="btn btn-default">Cancel</a>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <footer class="main-footer">
            <div class="pull-right hidden-xs">
                <b>Version</b> 2.0
            </div>
            <strong>Copyright &copy; 2014-2015 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights reserved.
        </footer>
    </div>

    <!-- Scripts -->
    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <script src="../../bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="../../plugins/slimScroll/jquery.slimscroll.min.js" type="text/javascript"></script>
    <script src="../../plugins/fastclick/fastclick.min.js"></script>
    <script src="../../dist/js/app.min.js" type="text/javascript"></script>
</body>
</html>

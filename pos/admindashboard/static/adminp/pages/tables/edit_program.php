<?php
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if ID is set and is numeric
if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    // Fetch the current program details from the database
    $sql = "SELECT * FROM program WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $department_name = $row['Department_Name'];
        $program_name = $row['Program_Name'];
        $duration = $row['Program_Duration'];
        $sem = $row['No_Of_Semester'];
        $fee = $row['Fee'];
    } else {
        // Redirect if program is not found
        header("Location: mprogram.php?error=notfound");
        exit;
    }

    $stmt->close();
} else {
    // Redirect if ID is not valid
    header("Location: mprogram.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Form submission logic
    $new_dname = $_POST['department_name'];  // Selected department name
    $new_pname = $_POST['program_name'];
    $new_duration = $_POST['duration'];
    $new_sem = $_POST['sem'];
    $new_fee = $_POST['fee'];

    // Update the program record in the database
    $stmt = $conn->prepare("UPDATE program SET Department_Name = ?, Program_Name = ?, Program_Duration = ?, No_Of_Semester = ?, Fee = ? WHERE id = ?");
    $stmt->bind_param("sssiis", $new_dname, $new_pname, $new_duration, $new_sem, $new_fee, $id);

    if ($stmt->execute()) {
        // Redirect to mprogram.php after success
        header("Location: mprogram.php?status=updated");
    } else {
        echo "<script>alert('Error updating program: " . $stmt->error . "');</script>";
    }

    $stmt->close();
}

// Fetch departments for the dropdown
$departments_sql = "SELECT Department_Name FROM department";
$departments_result = $conn->query($departments_sql);

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Edit Program</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css">
</head>
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
                    <b>Edit Program</b>
                </h1>
                <ol class="breadcrumb">
                    <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
                    <li><a href="#">Manage Programs</a></li>
                    <li><a href="#">Edit Program</a></li>
                </ol>
            </section>

            <!-- Main content -->
            <section class="content">
                <div class="row">
                    <div class="col-xs-12">
                        <div class="box">
                            <div class="box-header">
                                <h3 class="box-title">Edit Program Information</h3>
                            </div>

                            <div class="box-body">
                                <form action="edit_program.php?id=<?php echo $id; ?>" method="POST">
                                    <div class="form-group">
                                        <label for="department_name">Department Name</label>
                                        <select class="form-control" id="department_name" name="department_name" required>
                                            <option value="">Select Department</option>
                                            <?php
                                            // Populate the department dropdown
                                            if ($departments_result->num_rows > 0) {
                                                while ($dept = $departments_result->fetch_assoc()) {
                                                    $selected = ($department_name == $dept['Department_Name']) ? 'selected' : '';
                                                    echo "<option value='" . htmlspecialchars($dept['Department_Name']) . "' $selected>" . htmlspecialchars($dept['Department_Name']) . "</option>";
                                                }
                                            }
                                            ?>
                                        </select>
                                    </div>

                                    <div class="form-group">
                                        <label for="program_name">Program Name</label>
                                        <input type="text" class="form-control" id="program_name" name="program_name" value="<?php echo htmlspecialchars($program_name); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="duration">Program Duration</label>
                                        <input type="text" class="form-control" id="duration" name="duration" value="<?php echo htmlspecialchars($duration); ?>" required>
                                    </div>
                                    <div class="form-group">
                                       <label for="sem">No Of Semester</label>
                                       <input type="number" class="form-control" id="sem" name="sem" value="<?php echo htmlspecialchars($sem); ?>" required>
                                    </div>

                                    <div class="form-group">
                                        <label for="fee">Program Fee</label>
                                        <input type="number" class="form-control" id="fee" name="fee" value="<?php echo htmlspecialchars($fee); ?>" required>
                                    </div>
                                    <button type="submit" class="btn btn-success">Save Changes</button>
                                    <a href="mprogram.php" class="btn btn-default">Cancel</a>
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

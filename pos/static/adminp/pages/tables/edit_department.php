<?php
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if ID is set and is numeric
if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    // Fetch the current department details from the database
    $sql = "SELECT * FROM department WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $department_id = $row['Department_ID'];
        $name = $row['Department_Name'];
        $moto = $row['Department_Moto'];
    } else {
        // Redirect if department is not found
        header("Location: mdepartment.php?error=notfound");
        exit;
    }

    $stmt->close();
} else {
    // Redirect if ID is not valid
    header("Location: mdepartment.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Form submission logic
    $new_id = $_POST['department_id'];
    $new_name = $_POST['name'];
    $new_moto = $_POST['moto'];

    // Update the department record in the database
    $stmt = $conn->prepare("UPDATE department SET Department_ID = ?, Department_Name = ?, Department_Moto = ? WHERE id = ?");
    $stmt->bind_param("issi", $new_id, $new_name, $new_moto, $id);

    if ($stmt->execute()) {
        // Redirect to mdepartment.php after success
        header("Location: mdepartment.php?status=updated");
    } else {
        echo "<script>alert('Error updating department: " . $stmt->error . "');</script>";
    }

    $stmt->close();
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Edit Department</title>
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
                    <b>Edit Department</b>
                </h1>
                <ol class="breadcrumb">
                    <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
                    <li><a href="#">Manage Departments</a></li>
                    <li><a href="#">Edit Department</a></li>
                </ol>
            </section>

            <!-- Main content -->
            <section class="content">
                <div class="row">
                    <div class="col-xs-12">
                        <div class="box">
                            <div class="box-header">
                                <h3 class="box-title">Edit Department Information</h3>
                            </div>

                            <div class="box-body">
                                <form action="edit_department.php?id=<?php echo $id; ?>" method="POST">
                                    <div class="form-group">
                                        <label for="id">Department ID</label>
                                        <input type="text" class="form-control" id="department_id" name="department_id" value="<?php echo htmlspecialchars($department_id); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="name">Department Name</label>
                                        <input type="text" class="form-control" id="name" name="name" value="<?php echo htmlspecialchars($name); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="moto">Department Moto</label>
                                        <input type="text" class="form-control" id="moto" name="moto" value="<?php echo htmlspecialchars($moto); ?>" required>
                                    </div>
                                    <button type="submit" class="btn btn-success">Save Changes</button>
                                    <a href="mdepartment.php" class="btn btn-default">Cancel</a>
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

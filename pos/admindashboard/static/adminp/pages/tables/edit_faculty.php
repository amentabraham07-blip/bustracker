    <?php
    // Database connection
    $conn = mysqli_connect("localhost", "root", "", "college");

    // Check if ID is set
    if (isset($_GET['id']) && !empty($_GET['id'])) {
        $faculty_id = $_GET['id'];

        // Fetch the current course details from the database
        $sql = "SELECT * FROM faculty WHERE Faculty_ID = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("s", $faculty_id);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $fname = $row['Faculty_Name'];
            $photo = $row['Photo'];
            $dname = $row['Department_Name'];
            $qualification = $row['Qualification'];
            $address = $row['Address'];
            $email = $row['Email'];
            $phone = $row['Phone'];
        } else {
            // Redirect if course is not found
            header("Location: facultyrecord.php?error=notfound");
            exit;
        }

        $stmt->close();
    } else {
        // Redirect if ID is not valid
        header("Location: facultyrecord.php");
        exit;
    }

    // Handle form submission for updating course
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $new_fname = $_POST['fname'];
        $new_photo = $_POST['photo'];
        $new_dname = $_POST['dname'];
        $new_qualification = $_POST['qualification'];
        $new_address = $_POST['address'];
        $new_email = $_POST['email'];
        $new_phone = $_POST['phone'];


    
            // Update the course record
            $stmt = $conn->prepare("UPDATE faculty SET Faculty_Name = ?, Photo = ?, Department_Name = ?, Qualification = ?, Address = ?, Email = ?, Phone = ? WHERE Faculty_ID = ?");
            $stmt->bind_param("ssssssss", $new_fname, $new_photo, $new_dname, $new_qualification, $new_address, $new_email, $new_phone, $faculty_id);

            if ($stmt->execute()) {
                // Redirect after success
                header("Location: facultyrecord.php?status=updated");
            } else {
                echo "<script>alert('Error updating faculty record: " . $stmt->error . "');</script>";
            }
            $stmt->close();
        
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
                                    <form action="edit_faculty.php?id=<?php echo htmlspecialchars($faculty_id); ?>" method="POST">
                                        
                                        

                                        <!-- faculty name (Text Input) -->
                                        <div class="form-group">
                                            <label for="fname">Faculty Name</label>
                                            <input type="text" class="form-control" id="fname" name="fname" value="<?php echo htmlspecialchars($fname); ?>" required>
                                        </div>

                                        <!-- Photo Upload -->
                                        <div class="form-group">
                                            <label for="photo">Photo</label>
                                            <input type="file" class="form-control" id="photo" name="photo">
                                            <small>Current Photo: <?php echo $photo ? 'Yes' : 'No'; ?></small>
                                        </div>


                                        <!-- Department Field -->
                                        <div class="form-group">
                                            <select name="dname" class="form-control" id="dname" required>
                                                <option value="<?php echo htmlspecialchars($dname); ?>"><?php echo htmlspecialchars($dname); ?></option>
                                                <?php
                                                // Fetch department names from the database
                                                $sql = "SELECT Department_Name FROM department";
                                                $result = $conn->query($sql);
                                                if ($result->num_rows > 0) {
                                                    while ($row = $result->fetch_assoc()) {
                                                        echo "<option value='" . $row['Department_Name'] . "'>" . $row['Department_Name'] . "</option>";
                                                    }
                                                }
                                                ?>
                                            </select>
                                        </div>

                                        <!-- Qualification-->
                                        <div class="form-group">
                                            <label for="qualification">Qualification</label>
                                            <input type="text" class="form-control" id="qualification" name="qualification" value="<?php echo htmlspecialchars($qualification); ?>" required>
                                        </div>

                                        <!-- Address-->
                                        <div class="form-group">
                                            <label for="address">Address</label>
                                            <input type="text" class="form-control" id="address" name="address" value="<?php echo htmlspecialchars($address); ?>" required>
                                        </div>

                                        <!-- Address-->
                                        <div class="form-group">
                                            <label for="email">Email</label>
                                            <input type="text" class="form-control" id="email" name="email" value="<?php echo htmlspecialchars($email); ?>" required>
                                        </div>

                                        <!-- Address-->
                                        <div class="form-group">
                                            <label for="phone">Email</label>
                                            <input type="text" class="form-control" id="phone" name="phone" value="<?php echo htmlspecialchars($phone); ?>" required>
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

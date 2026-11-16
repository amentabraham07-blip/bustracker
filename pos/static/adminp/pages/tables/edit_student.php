<?php
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if ID is set and is numeric
if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    // Fetch the current student details from the database
    $sql = "SELECT * FROM student WHERE Admission_NO = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $admission_no = $row['Admission_NO'];
        $name = $row['Name'];
        $department = $row['Department_Name'];
        $program = $row['Program_Name'];
        $semester = $row['Current_Semester'];
        $address = $row['Address'];
        $dob = $row['DOB'];
        $blood_group = $row['Blood_Group'];
        $email = $row['Email'];
        $phone_no = $row['Phone_No'];
        $year_of_admission = $row['Year_Of_Admission'];
        $photo = $row['Photo'];
    } else {
        // Redirect if student is not found
        header("Location: studentrecord.php?error=notfound");
        exit;
    }

    $stmt->close();
} else {
    // Redirect if ID is not valid
    header("Location: studentrecord.php");
    exit;
}

// Handle form submission to update student details
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Collect the new data from the form
    $new_admission_no = $_POST['admission_no'];
    $new_name = $_POST['name'];
    $new_department = $_POST['department'];
    $new_program = $_POST['program'] ? $_POST['program'] : $program;  // Use old program if no new program is selected
    $new_semester = $_POST['semester'] ? $_POST['semester'] : $semester;  // Use old semester if no new semester is selected
    $new_address = $_POST['address'];
    $new_dob = $_POST['dob'];
    $new_blood_group = $_POST['blood_group'];
    $new_email = $_POST['email'];
    $new_phone_no = $_POST['phone_no'];
    $new_year_of_admission = $_POST['year_of_admission'];
    $new_photo = $_FILES['photo']['name'] ? 'uploads/' . $_FILES['photo']['name'] : $photo;

    // Check for duplicate Admission_NO (make sure the Admission_NO is unique)
    $sql_check = "SELECT COUNT(*) FROM student WHERE Admission_NO = ? AND Admission_NO != ?";
    $stmt_check = $conn->prepare($sql_check);
    $stmt_check->bind_param("ii", $new_admission_no, $admission_no);
    $stmt_check->execute();
    $stmt_check->bind_result($count);
    $stmt_check->fetch();
    $stmt_check->close();

    if ($count > 0) {
        echo "<script>alert('Error: Admission Number already exists!');</script>";
    } else {
        // If the photo is uploaded, move the file to the desired folder
        if ($_FILES['photo']['name']) {
            move_uploaded_file($_FILES['photo']['tmp_name'], $new_photo);
        }

        // Update the student record in the database
        $stmt = $conn->prepare("UPDATE student SET Admission_NO = ?, Name = ?, Department_Name = ?, Program_Name = ?, Current_Semester = ?, Address = ?, DOB = ?, Blood_Group = ?, Email = ?, Phone_No = ?, Year_Of_Admission = ?, Photo = ? WHERE Admission_NO = ?");
        $stmt->bind_param("issssssssssss", $new_admission_no, $new_name, $new_department, $new_program, $new_semester, $new_address, $new_dob, $new_blood_group, $new_email, $new_phone_no, $new_year_of_admission, $new_photo, $admission_no);

        if ($stmt->execute()) {
            // Redirect to student record page after success
            header("Location: studentrecord.php?status=updated");
        } else {
            echo "<script>alert('Error updating student: " . $stmt->error . "');</script>";
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
    <title>Edit Student</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css">
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css">
</head>
<?php
$conn = mysqli_connect("localhost", "root", "", "college");
?>
<body class="skin-blue">
    <div class="wrapper">
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

        <div class="content-wrapper">
            <section class="content-header">
                <h1>Edit Student</h1>
                <ol class="breadcrumb">
                    <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
                    <li><a href="#">Manage Students</a></li>
                    <li><a href="#">Edit Student</a></li>
                </ol>
            </section>

            <section class="content">
                <div class="row">
                    <div class="col-xs-12">
                        <div class="box">
                            <div class="box-header">
                                <h3 class="box-title">Edit Student Information</h3>
                            </div>
                            <div class="box-body">
                                <form action="edit_student.php?id=<?php echo $admission_no; ?>" method="POST" enctype="multipart/form-data">
                                    <!-- Admission Number Field -->
                                    <div class="form-group">
                                        <label for="admission_no">Admission Number</label>
                                        <input type="text" class="form-control" id="admission_no" name="admission_no" value="<?php echo htmlspecialchars($admission_no); ?>" required>
                                    </div>

                                    <!-- Name Field -->
                                    <div class="form-group">
                                        <label for="name">Name</label>
                                        <input type="text" class="form-control" id="name" name="name" value="<?php echo htmlspecialchars($name); ?>" required>
                                    </div>

                                    <!-- Department Field -->
                                    <div class="form-group">
                                        <select name="department" class="form-control" id="dname" required>
                                            <option value="<?php echo htmlspecialchars($department); ?>"><?php echo htmlspecialchars($department); ?></option>
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

                                    <!-- Program Field -->
                                    <div class="form-group">
                                        <select name="program" class="form-control" id="pname" required>
                                            <option value="<?php echo $program; ?>"><?php echo $program ? $program : 'Select Program'; ?></option>
                                        </select>
                                    </div>

                                    <!-- Semester Field -->
                                    <div class="form-group">
                                        <select name="semester" class="form-control" id="sem" required>
                                            <option value="<?php echo $semester; ?>"><?php echo $semester ? $semester : 'Select Semester'; ?></option>
                                        </select>
                                    </div>

                                    <!-- Other Fields (Address, DOB, Blood Group, etc.) -->
                                    <div class="form-group">
                                        <label for="address">Address</label>
                                        <textarea class="form-control" id="address" name="address" rows="3"><?php echo htmlspecialchars($address); ?></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="dob">Date of Birth</label>
                                        <input type="date" class="form-control" id="dob" name="dob" value="<?php echo $dob; ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="blood_group">Blood Group</label>
                                        <input type="text" class="form-control" id="blood_group" name="blood_group" value="<?php echo htmlspecialchars($blood_group); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" class="form-control" id="email" name="email" value="<?php echo htmlspecialchars($email); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="phone_no">Phone No</label>
                                        <input type="text" class="form-control" id="phone_no" name="phone_no" value="<?php echo htmlspecialchars($phone_no); ?>" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="year_of_admission">Year of Admission</label>
                                        <input type="text" class="form-control" id="year_of_admission" name="year_of_admission" value="<?php echo htmlspecialchars($year_of_admission); ?>" required>
                                    </div>

                                    <!-- Photo Upload -->
                                    <div class="form-group">
                                        <label for="photo">Photo</label>
                                        <input type="file" class="form-control" id="photo" name="photo">
                                        <small>Current Photo: <?php echo $photo ? 'Yes' : 'No'; ?></small>
                                    </div>

                                    <!-- Save and Cancel Buttons -->
                                    <button type="submit" class="btn btn-success">Save Changes</button>
                                    <a href="studentrecord.php" class="btn btn-default">Cancel</a>
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

    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <script src="../../bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="../../plugins/slimScroll/jquery.slimscroll.min.js" type="text/javascript"></script>
    <script src="../../plugins/fastclick/fastclick.min.js"></script>
    <script src="../../dist/js/app.min.js" type="text/javascript"></script>

    <script>
        $(document).ready(function() {
            // Department Change event to populate Programs
            $('#dname').on('change', function() {
                var department = $(this).val();
                $.ajax({
                    url: 'getprogram.php',
                    type: 'POST',
                    data: { Department_Name: department },
                    success: function(response) {
                        $('#pname').html(response);
                        $('#sem').html("<option value=''>Select Semester</option>"); // Reset semester dropdown
                    }
                });
            });

            // Program Change event to populate Semesters
            $('#pname').on('change', function() {
                var program = $(this).val();
                $.ajax({
                    url: 'getsem.php',
                    type: 'POST',
                    data: { Program_Name: program },
                    success: function(response) {
                        $('#sem').html(response); // Populate semester dropdown
                    }
                });
            });
        });
    </script>
</body>
</html>

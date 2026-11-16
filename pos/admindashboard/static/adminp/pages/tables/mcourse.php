<?php
$conn = mysqli_connect("localhost", "root", "", "college");

// Check if the connection is successful
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>AdminLTE 2 | Manage Courses</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <!-- Bootstrap 3.3.2 -->
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- Font Awesome Icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons -->
    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />
    <!-- AdminLTE Skins -->
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css" />
  </head>
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
          <h1><b>Manage Courses</b></h1>
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Manage Courses</a></li>
          </ol>
        </section>

        <section class="content">
          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                  <h3 class="box-title">Records of Courses</h3>
                </div>

                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                      <th>Program</th>
                      <th>Course Code</th>
                      <th>Course Name</th>
                      <th>Duration</th>
                      <th>Edit</th>
                      <th>Delete</th>
                    </tr>

                    <?php
                    // Fetching course records from the database
                    $sql = "SELECT * FROM course";
                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        while ($row = $result->fetch_assoc()) {
                            ?>
                            <tr>
                              <td><?php echo $row['Program_Name']; ?></td>
                              <td><?php echo $row['Course_Code']; ?></td>
                              <td><?php echo $row['Course_Name']; ?></td>
                              <td><?php echo $row['Duration']; ?></td>
                              <td>
                                <a href="edit_course.php?id=<?php echo $row['Course_Code']; ?>&department_name=<?php echo urlencode($row['Department_Name']); ?>&program_name=<?php echo urlencode($row['Program_Name']); ?>&sem=<?php echo urlencode($row['semester']); ?>&ccode=<?php echo urlencode($row['Course_Code']); ?>&cname=<?php echo urlencode($row['Course_Name']); ?>&duration=<?php echo urlencode($row['Duration']); ?>">
                                  <button class="btn btn-primary">Edit</button>
                                </a>
                              </td>
                              <td>
                                <a href="javascript:void(0);" onclick="confirmDelete('<?php echo $row['Course_Code']; ?>');">
                                  <button class="btn btn-danger">Delete</button>
                                </a>
                              </td>
                            </tr>
                            <?php
                        }
                    }
                    ?>

                  </table>
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
        <strong>&copy; 2014-2015 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights reserved.
      </footer>

    </div>

    <!-- jQuery -->
    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <!-- Bootstrap JS -->
    <script src="../../bootstrap/js/bootstrap.min.js"></script>
    <!-- AdminLTE App -->
    <script src="../../dist/js/app.min.js"></script>

    <!-- Confirmation Script -->
    <script type="text/javascript">
      function confirmDelete(courseId) {
        // Show confirmation dialog
        var result = confirm("Are you sure you want to delete this course?");
        
        // If user clicks "OK", delete the course
        if (result) {
          window.location.href = "delete_course.php?id=" + courseId;
        }
      }
    </script>
  </body>
</html>

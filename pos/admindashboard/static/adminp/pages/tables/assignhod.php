<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>AdminLTE 2 | Simple Tables</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <!-- Bootstrap 3.3.2 -->
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- Font Awesome Icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons -->
    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />
    <!-- AdminLTE Skins. Choose a skin from the css/skins 
         folder instead of downloading all of them to reduce the load. -->
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css" />

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>
  <?php
  $conn = mysqli_connect("localhost", "root", "", "college");

  // Fetching the departments
  $departmentQuery = "SELECT Department_Name FROM department";
  $departments = $conn->query($departmentQuery);

  // Department filter if applied
  $departmentFilter = "";
  if (isset($_GET['department']) && !empty($_GET['department'])) {
    $departmentFilter = " AND Department_Name = '" . $_GET['department'] . "'";
  }

  // SQL query for fetching records based on Rights
  $sql = "SELECT * FROM faculty WHERE Rights IN ('Faculty', 'HOD', 'ClassInCharge')" . $departmentFilter;
  $result = $conn->query($sql);
  ?>
  <body class="skin-blue">
    <div class="wrapper">

      <header class="main-header">
        <a href="../../index2.html" class="logo"><b>MES</b>College</a>
        <!-- Header Navbar: style can be found in header.less -->
        <nav class="navbar navbar-static-top" role="navigation">
          <div class="navbar-custom-menu">
            <ul class="nav navbar-nav">
              <!-- User Account: style can be found in dropdown.less -->
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
          <h1><b>Faculty Records</b></h1>
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Faculty Records</a></li>
          </ol>
        </section>

        <section class="content">
          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                  <h3 class="box-title">Filter Faculty Records by Department</h3>
                  <form method="GET" action="">
                    <select name="department" class="form-control" style="width: 200px; display: inline-block;">
                      <option value="">Select Department</option>
                      <?php while ($row = $departments->fetch_assoc()) { ?>
                        <option value="<?php echo $row['Department_Name']; ?>"><?php echo $row['Department_Name']; ?></option>
                      <?php } ?>
                    </select>
                    <button type="submit" class="btn btn-primary">Filter</button>
                  </form>
                </div><!-- /.box-header -->

                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                      <th>Faculty ID</th>
                      <th>Faculty Name</th>
                      <th>Photo</th>
                      <th>Applied Department</th>
                      <th>Qualification</th>
                      <th>Address</th>
                      <th>Email</th>
                      <th>Phone No</th>
                      <th>Status</th>
                      <th></th>
                    </tr>

                    <?php
                    if ($result->num_rows > 0) {
                      while ($row = $result->fetch_assoc()) {
                        ?>
                        <tr>
                          <td><?php echo $row['Faculty_ID']; ?></td>
                          <td><?php echo htmlspecialchars($row['Faculty_Name']); ?></td>
                          <td>
                            <?php
                            if (!empty($row['Photo'])) {
                              echo "<img src='" . htmlspecialchars($row['Photo']) . "' alt='Faculty Photo' style='width:50px; height:50px;' />";
                            } else {
                              echo "No Image";
                            }
                            ?>
                          </td>
                          <td><?php echo htmlspecialchars($row['Department_Name']); ?></td>
                          <td><?php echo htmlspecialchars($row['Qualification']); ?></td>
                          <td><?php echo htmlspecialchars($row['Address']); ?></td>
                          <td><?php echo htmlspecialchars($row['Email']); ?></td>
                          <td><?php echo htmlspecialchars($row['Phone']); ?></td>
                          <td><?php echo htmlspecialchars($row['Rights']); ?></td>
                          <td>
                            <button class="btn btn-success" onclick="assignHOD('<?php echo $row['Faculty_ID']; ?>', '<?php echo $row['Department_Name']; ?>')">Assign as HOD</button>
                          </td>
                        </tr>
                        <?php
                      }
                    }
                    ?>
                  </table>
                </div><!-- /.box-body -->
              </div><!-- /.box -->
            </div>
          </div>
        </section>
      </div><!-- /.content-wrapper -->

      <footer class="main-footer">
        <div class="pull-right hidden-xs">
          <b>Version</b> 2.0
        </div>
        <strong>Copyright &copy; 2014-2015 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights reserved.
      </footer>
    </div><!-- ./wrapper -->

    <!-- jQuery 2.1.3 -->
    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <!-- Bootstrap 3.3.2 JS -->
    <script src="../../bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
    <!-- Slimscroll -->
    <script src="../../plugins/slimScroll/jquery.slimscroll.min.js" type="text/javascript"></script>
    <!-- FastClick -->
    <script src='../../plugins/fastclick/fastclick.min.js'></script>
    <!-- AdminLTE App -->
    <script src="../../dist/js/app.min.js" type="text/javascript"></script>

    <script>
      function assignHOD(facultyID, department) {
        if (confirm('Are you sure you want to assign this faculty as HOD?')) {
          // Revert the current HOD if any in the same department
          $.ajax({
            url: 'assign_hod.php',
            type: 'POST',
            data: {
              facultyID: facultyID,
              department: department
            },
            success: function(response) {
              alert(response);
              location.reload();  // Reload the page after action
            }
          });
        }
      }
    </script>
  </body>
</html>

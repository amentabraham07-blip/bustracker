<?php
$conn = mysqli_connect("localhost", "root", "", "college");
?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>AdminLTE 2 | Manage Departments</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <!-- Bootstrap 3.3.2 -->
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- Font Awesome Icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons -->
    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css" />
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
                  <span class="hidden-xs"><b>Admin@MESErumely</span>
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
            <b>Manage Departments</b>
          </h1>
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Manage Departments</a></li>
          </ol>
        </section>

        <!-- Main content -->
        <section class="content">
          <!-- Success Message -->
          <?php
          if (isset($_GET['status']) && $_GET['status'] == 'updated') {
            echo "<script type='text/javascript'>
                    alert('Department updated successfully!');
                  </script>";
          }
          ?>

          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                  <h3 class="box-title">Records Of Departments</h3>
                </div>
                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                      <th>Department ID</th>
                      <th>Department Name</th>
                      <th>Department Moto</th>
                      <th>Edit</th>
                      <th>Delete</th>
                    </tr>
                    <?php
                    // Fetching department records
                    $sql = "SELECT * FROM department";
                    $result = $conn->query($sql);
                    if ($result->num_rows > 0) {
                      while ($row = $result->fetch_assoc()) {
                        $id = $row['id'];
                        ?>
                        <tr>
                          <td><?php echo $row['Department_ID']; ?></td>
                          <td><?php echo $row['Department_Name']; ?></td>
                          <td><?php echo $row['Department_Moto']; ?></td>
                          <td>
                            <!-- Edit button -->
                            <a href="edit_department.php?id=<?php echo $row['id']; ?>&department_id=<?php echo urlencode($row['Department_ID']); ?>&name=<?php echo urlencode($row['Department_Name']); ?>&moto=<?php echo urlencode($row['Department_Moto']); ?>">
                              <button class="btn btn-primary">Edit</button>
                            </a>
                          </td>
                          <td>
                            <!-- Delete button -->
                            <a href="delete_department.php?id=<?php echo $row['id']; ?>" onclick="return confirm('Are you sure you want to delete this department?');">
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
        <strong>Copyright &copy; 2014-2015 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights reserved.
      </footer>
    </div>

    <!-- Scripts -->
    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <script src="../../bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="../../plugins/slimScroll/jquery.slimscroll.min.js" type="text/javascript"></script>
    <script src="../../plugins/fastclick/fastclick.min.js"></script>
    <script src="../../dist/js/app.min.js" type="text/javascript"></script>
    <script type="text/javascript">
  function confirmDelete(departmentId) {
    // Show a confirmation dialog
    var result = confirm("Are you sure you want to delete this department?");
    
    // If the user clicked "OK", redirect to the delete_department.php page
    if (result) {
      window.location.href = "delete_department.php?id=" + departmentId;
    }
  }
</script>
  </body>
</html>

<?php
$conn->close();
?>

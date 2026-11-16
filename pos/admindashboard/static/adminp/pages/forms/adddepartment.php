<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>AdminLTE 2 | Dashboard</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <link href="../../bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <link href="../../dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css" />
  </head>
  <?php
  $conn = mysqli_connect("localhost", "root", "", "college");

  if (isset($_POST['submit'])) {
    $m1 = $_POST["t1"]; // Department ID
    $m2 = $_POST["t2"]; // Department Name
    $m3 = $_POST["t3"]; // Department Moto

    // Check if Department ID or Department Name already exists
    $checkQuery = "SELECT * FROM department WHERE Department_ID = '$m1' OR Department_Name = '$m2'";
    $checkResult = mysqli_query($conn, $checkQuery);
    
    $idExists = false;
    $nameExists = false;

    // Check if Department ID exists
    $checkIDQuery = "SELECT * FROM department WHERE Department_ID = '$m1'";
    $idResult = mysqli_query($conn, $checkIDQuery);
    if (mysqli_num_rows($idResult) > 0) {
        $idExists = true;
    }

    // Check if Department Name exists
    $checkNameQuery = "SELECT * FROM department WHERE Department_Name = '$m2'";
    $nameResult = mysqli_query($conn, $checkNameQuery);
    if (mysqli_num_rows($nameResult) > 0) {
        $nameExists = true;
    }

    // Show appropriate alert based on existence of Department ID or Name
    if ($idExists && $nameExists) {
        echo "<script>alert('Both Department ID and Department Name already exist.');</script>";
    } elseif ($idExists) {
        echo "<script>alert('Department ID already exists.');</script>";
    } elseif ($nameExists) {
        echo "<script>alert('Department Name already exists.');</script>";
    } else {
        // If both values do not exist, proceed with the insert
        $insertQuery = "INSERT INTO department (Department_ID, Department_Name, Department_Moto) 
                        VALUES ('$m1', '$m2', '$m3')";
        $insertResult = mysqli_query($conn, $insertQuery);

        if ($insertResult) {
            echo "<script>alert('Department added successfully.');</script>";
        } else {
            echo "<script>alert('Error adding department.');</script>";
        }
    }
  }
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
                  <span class="hidden-xs"><b>Admin@MESErumely</span>
                </a>
                <ul class="dropdown-menu">
                  <li class="user-header">
                    <img src="../../dist/img/user2-160x160.jpg" class="img-circle" alt="User Image" />
                    <p>
                      Admin@MESErumely
                    </p>
                  </li>
                  <li class="user-footer">
                    <div class="pull-left">
                      <a href="#" class="btn btn-default btn-flat">Profile</a>
                    </div>
                    <div class="pull-right">
                      <a href="#" class="btn btn-default btn-flat">Sign out</a>
                    </div>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </nav>
      </header>

      <div class="content-wrapper">
        <section class="content-header">
          <h1>Add Department</h1>
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Add Departments</a></li>
          </ol>
        </section>

        <section class="content">
          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                  <h3 class="box-title">Enter Department Details</h3>
                </div>
                <div class="box-body table-responsive no-padding">
                  <form action="" method="POST">
                    <table class="table table-hover">
                      <tr>
                        <th>Department ID</th>
                        <th>Department Name</th>
                        <th>Department Moto</th>
                        <th></th>
                      </tr>
                      <tr>
                        <td>
                          <div class="form-group">
                            <input type="int" name="t1" class="form-control" id="did" placeholder="Enter Department ID">
                          </div>
                        </td>
                        <td>
                          <div class="form-group">
                            <input type="text" name="t2" class="form-control" id="dname" placeholder="Enter Department Name">
                          </div>
                        </td>
                        <td>
                          <div class="form-group">
                            <input type="text" name="t3" class="form-control" id="dmoto" placeholder="Enter Department Moto">
                          </div>
                        </td>
                        <td>
                          <button type="submit" name="submit" id="adddepartment" class="btn btn-primary">Add Department</button>
                        </td>
                      </tr>
                    </table>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <!-- Display departments -->
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
                    </tr>
                    <?php
                    $result = mysqli_query($conn, "SELECT * FROM department ORDER BY Department_ID DESC");
                    while ($row = mysqli_fetch_assoc($result)) {
                    ?>
                    <tr>
                      <td><?php echo $row['Department_ID']; ?></td>
                      <td><?php echo $row['Department_Name']; ?></td>
                      <td><?php echo $row['Department_Moto']; ?></td>
                    </tr>
                    <?php
                    }
                    mysqli_close($conn);
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
        <strong>&copy; 2024<a href="http://almsaeedstudio.com">MES COLLEGE ERUMELY</a>.</strong> All rights reserved.
      </footer>
    </div>

    <script src="../../plugins/jQuery/jQuery-2.1.3.min.js"></script>
    <script src="../../bootstrap/js/bootstrap.min.js"></script>
    <script src="../../plugins/fastclick/fastclick.min.js"></script>
    <script src="../../dist/js/app.min.js"></script>
    <script src="../../dist/js/demo.js"></script>
  </body>
</html>

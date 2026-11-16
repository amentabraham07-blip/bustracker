<?php
$conn = mysqli_connect("localhost", "root", "", "college"); // Establishing database connection
?>
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
    <!-- AdminLTE Skins -->
    <link href="../../dist/css/skins/_all-skins.min.css" rel="stylesheet" type="text/css" />
    <!-- jQuery Confirmation -->
    <script type="text/javascript">
        // Confirm approval action
        function confirmApproval() {
            return confirm("Are you sure you want to approve this faculty?");
        }

        // Confirm rejection action
        function confirmRejection() {
            return confirm("Are you sure you want to reject this faculty?");
        }
    </script>
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
                            <ul class="dropdown-menu">
                                <li class="user-header">
                                    <img src="../../dist/img/user2-160x160.jpg" class="img-circle" alt="User Image" />
                                    <p>Admin@MESErumely</p>
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
                                <h3 class="box-title">Record Of Current Faculties</h3>
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
                                        <th></th>
                                        <th></th>
                                    </tr>
                                    <?php
                                    // Fetching faculty data with pending status
                                    $sql = "SELECT * FROM faculty WHERE Rights='Pending'";
                                    $result = $conn->query($sql);

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
                                                <td>
                                                    <!-- Reject button with confirmation -->
                                                    <a href="rejectfaculty.php?id=<?php echo $row['Faculty_ID']; ?>" onclick="return confirmRejection();">
                                                        <button class="btn btn-primary">Reject</button>
                                                    </a>
                                                </td>
                                                <td>
                                                    <!-- Approve button with confirmation -->
                                                    <a href="approvefaculty.php?id=<?php echo $row['Faculty_ID']; ?>" onclick="return confirmApproval();">
                                                        <button class="btn btn-danger">Approve</button>
                                                    </a>
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
        </div>

        <footer class="main-footer">
            <div class="pull-right hidden-xs">
                <b>Version</b> 2.0
            </div>
            <strong>Copyright &copy; 2014-2015 <a href="http://almsaeedstudio.com">Almsaeed Studio</a>.</strong> All rights reserved.
        </footer>
    </div>

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
    <!-- AdminLTE for demo purposes -->
    <script src="../../dist/js/demo.js" type="text/javascript"></script>
</body>
</html>

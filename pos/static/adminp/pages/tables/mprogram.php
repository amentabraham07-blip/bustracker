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
  $conn=mysqli_connect("localhost","root","","college");
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
                  <span class="hidden-xs"><b>Admin@MESErumely</span>
                </a>
                <ul class="dropdown-menu">
                  <!-- User image -->
                  <li class="user-header">
                    <img src="../../dist/img/user2-160x160.jpg" class="img-circle" alt="User Image" />
                    <p>
                      Admin@MESErumely
                      
                    </p>
                  </li>
                  <!-- Menu Body -->
                 
                  <!-- Menu Footer-->
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
     

      <!-- Right side column. Contains the navbar and content of the page -->
      <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        <section class="content-header">
            
          <h1>
            Manage Programs
            <div>
            <small></small>
    </div>
    </h1>
            
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Manage Programs</a></li>
            
          </ol>
        </section>

        <!-- Main content -->
        <section class="content">
          <!-- Success Message -->
          <?php
          if (isset($_GET['status']) && $_GET['status'] == 'updated') {
            echo "<script type='text/javascript'>
                    alert('Program updated successfully!');
                  </script>";
          }
          ?>

             
           

          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                <h3 class="box-title">Records Of Programs</h3>
                  <div class="box-tools">
                     </div>
                  </div>
                  
                </div><!-- /.box-header -->
                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                      
                      <th>Department Name</th>
                      <th>Program Name</th>
                      <th>Program Duration</th>
                      <th>No Of Semester</th>
                      <th>Program Fee</th>
                      <th></th>
                      
                    </tr>
                    <?php 
                  
              
                    
                    $sql=("select *  from program  ");
                  $result=$conn->query($sql);
                  if($result->num_rows > 0)
                {
                  while($row = $result->fetch_assoc())
                {
                ?>
                    <tr>
                      
                      <td><?php echo $row['Department_Name']; ?></td>
                      <td><?php echo $row['Program_Name']; ?></td>
                      <td><?php echo $row['Program_Duration']; ?></td>
                      <td><?php echo $row['No_Of_Semester']; ?></td>
                      <td><?php echo $row['Fee']; ?></td>
                      <td>
                            <!-- Edit button -->
                            <a href="edit_program.php?id=<?php echo $row['id']; ?>&department_name=<?php echo urlencode($row['Department_Name']); ?>&program_name=<?php echo urlencode($row['Program_Name']); ?>&duration=<?php echo urlencode($row['Program_Duration']); ?>&sem=<?php echo urlencode($row['No_Of_Semester']); ?>&fee=<?php echo urlencode($row['Fee']); ?>">
                              <button class="btn btn-primary">Edit</button>
                            </a>
                          </td>
                          <td>
                            <!-- Delete button -->
                            <a href="delete_program.php?id=<?php echo $row['id']; ?>" onclick="return confirm('Are you sure you want to delete this program?');">
                              <button class="btn btn-danger">Delete</button>
                            </a>
                          </td>
                   </tr>
                   <?php 
                   }
                  }
                
                 $conn->close();
                ?>
                    
                  </table>
                </div><!-- /.box-body -->
              </div><!-- /.box -->
            </div>
          </div>
        </section><!-- /.content -->
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
    <!-- AdminLTE for demo purposes -->
    <script src="../../dist/js/demo.js" type="text/javascript"></script>
    <script type="text/javascript">
  function confirmDelete(programId) {
    // Show a confirmation dialog
    var result = confirm("Are you sure you want to delete this program?");
    
    // If the user clicked "OK", redirect to the delete_department.php page
    if (result) {
      window.location.href = "delete_department.php?id=" + programId;
    }
  }
</script>
  </body>
</html>

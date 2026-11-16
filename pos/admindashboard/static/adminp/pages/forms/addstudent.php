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
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

    <![endif]-->
  </head>
  <?php
  $conn=mysqli_connect("localhost","root","","college");
  if(isset($_POST['submit']))
  {
    $m1=$_POST["t1"];
    $m2=$_POST["t2"];
    $m3=$_POST["t3"];
    $m4=$_POST["t4"];
    $m5=$_POST["t5"];
    $m6=$_POST["t6"];
    $m7=$_POST["t7"];
    $m8=$_POST["t8"];
    $m9=$_POST["t9"];
    $m10=$_POST["t10"];
    $m11=$_POST["t11"];
    $m12=$_POST["t12"];
   
   // Check if Admission_NO already exists
   $checkQuery = "SELECT * FROM student WHERE Admission_NO = '$m1'";
   $result = mysqli_query($conn, $checkQuery);

   if (mysqli_num_rows($result) > 0) {
       // If the Admission_NO exists, show an alert and stop the form submission
       echo "<script>alert('Admission No already exists!');</script>";
   } else {
       // Insert new record if Admission_NO does not exist
       $n = mysqli_query($conn, "INSERT INTO student (Admission_NO, Name, Photo, Department_Name, Program_Name, Current_Semester, Address, DOB, Blood_Group, Email, Phone_No, Year_Of_Admission, Rights, Username, password)
       VALUES ('$m1', '$m2', '$m3', '$m4', '$m5', '$m6', '$m7', '$m8', '$m9', '$m10', '$m11', '$m12', 'student', '$m10', '$m11')");

       if ($n) {
           echo "<script>alert('Student record added successfully!');</script>";
       }
   }
 }
    
  
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
            <b>Add Student</b>
            <div>
              <small></small>
    </div>
    </h1>
            
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Add student</a></li>
            
          </ol>
        </section>

        <!-- Main content -->
        <section class="content">
          

             
           

          <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                <h3 class="box-title">Add New Student Record</h3>
                  <div class="box-tools">
                    
                    </div>
                  </div>
                  
                </div><!-- /.box-header -->
                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                      <th>Admission No</th>
                      <th>Name</th>
                      <th>Photo</th>
                      <th>Department</th>
                      <th>Program</th>
                      <th>Current Semester</th>
                      <th>Adress</th>
                      <th>DOB</th>
                      <th>Blood Group</th>            
                      <th>Email </th>
                      <th>Phone No </th>
                      <th>Year Of Admission<th>
                      <th></th>
                      
                      
                    </tr>
                    <form action="" method="POST">
    <tr>
        <td>
            <div class="form-group">
                <input type="int" class="form-control" id="adminno" name="t1" placeholder="Enter Admission No">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="text" class="form-control" id="name" name="t2" placeholder="Enter Name">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="file" name="t3" id="exampleInputFile">
            </div>
        </td>

        <td>
            <div class="form-group">
                <select name="t4" class="form-control" id="dname" placeholder="Select Department">
                    <option value="">Select Department</option>
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
        </td>

        <td>
            <div class="form-group">
                <select name="t5" class="form-control" id="pname" placeholder="Select Program">
                    <option value="">Select Program</option>
                </select>
            </div>
        </td>

        <td>
            <div class="form-group">
                <select name="t6" class="form-control" id="sem" placeholder="Select Semester">
                    <option value="">Select Semester</option>
                </select>
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="text" class="form-control" id="address" name="t7" placeholder="Enter Address">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="date" class="form-control" id="dob" name="t8" placeholder="Enter DOB">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="text" class="form-control" id="bloodgroup" name="t9" placeholder="Enter Blood Group">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="email" class="form-control" id="email" name="t10" placeholder="Enter Email">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="int" class="form-control" id="phoneno" name="t11" placeholder="Enter Phone No">
            </div>
        </td>

        <td>
            <div class="form-group">
                <input type="text" class="form-control" id="year" name="t12" placeholder="Enter Year Of Admission">
            </div>
        </td>

        <td>
            <button type="submit" id="addstudent" name="submit" class="btn btn-primary">Add Student</button>
        </td>
    </tr>
</form>
                    
                  </table>
                </div><!-- /.box-body -->
              </div><!-- /.box -->
              <section class="content">
              <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                <h3 class="box-title">Record Of Added Students</h3>
                  <div class="box-tools">
                    
                    </div>
                  </div>
                  
                </div><!-- /.box-header -->
                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                    <th>Admission No</th>
                      <th>Name</th>
                      <th>Photo</th>
                      <th>Department</th>
                      <th>Program</th>
                      <th>Current Semester</th>
                      <th>Adress</th>
                      <th>DOB</th>
                      <th>Blood Group</th>            
                      <th>Email </th>
                      <th>Phone No </th>
                      <th>Year Of Admission<th>
                      <centre><th>Usrename</th></centre>
                      <th></th>
                                            
                    </tr>
                    <tr>
                    <?php 
                        $sql = "SELECT * FROM student ORDER BY Admission_NO DESC";
                        $result = $conn->query($sql);

                        if ($result->num_rows > 0) {
                            while ($row = $result->fetch_assoc()) {
                                ?>
                                <tr>
                                    <td><?php echo $row['Admission_NO']; ?></td>
                                    <td><?php echo htmlspecialchars($row['Name']); ?></td>
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
                                    <td><?php echo htmlspecialchars($row['Program_Name']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Current_Semester']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Address']); ?></td>
                                    <td><?php echo htmlspecialchars($row['DOB']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Blood_Group']); ?></td>
                                     <td><?php echo htmlspecialchars($row['Email']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Phone_No']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Year_Of_Admission']); ?></td>
                                    <td><?php echo htmlspecialchars($row['Username']); ?></td>
                                </tr>
                                <?php 
                            }
                        }
                        ?>
                  </table>
                </div><!-- /.box-body -->
              </div><!-- /.box -->
    </section>
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
    <script>
	$(document).ready(function() {
    $('#dname').on('change', function() {
        var Department = $(this).val();
        $.ajax({
            url: 'getprogram.php',
            type: 'POST',
            data: { Department_Name: Department },
            success: function(response) {
                $('#pname').html(response);
                $('#sem').html("<option value=''>Select Semester</option>"); // Reset semester dropdown
            }
        });
    });

    $('#pname').on('change', function() {
        var Program = $(this).val();
        $.ajax({
            url: 'getsem.php',
            type: 'POST',
            data: { Program_Name: Program },
            success: function(response) {
                $('#sem').html(response); // Populate semester dropdown
            }
        });
    });
});

  </script>
  </body>
</html>

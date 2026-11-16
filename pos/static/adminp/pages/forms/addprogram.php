<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>AdminLTE 2 | Dashboard</title>
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
  if(isset($_POST['submit']))
  {
    $m1=$_POST["t1"];
    $m2=$_POST["t2"];
    $m3=$_POST["t3"];
    $m4=$_POST["t4"];
    $m5=$_POST["t5"];
    $n=mysqli_query($conn,"insert into program (Department_Name,Program_Name,Program_Duration,No_Of_Semester,Fee)values ('$m1','$m2','$m3','$m4','$m5')");
    if($n>0)
    ?>
    <?php
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
                      Alexander Pierce - Web Developer
                      <small>Member since Nov. 2012</small>
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
            Add Program
    </h1>
            
          <ol class="breadcrumb">
            <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Add Program</a></li>
            
          </ol>
        </section>
      

        <!-- Main content -->
        <section class="content">
          
              <div>
                 <!-- Main content -->
        <section class="content">
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
                    <form  action="" method="POST" class="form-control">
                    <tr>
                     <td>
                      <div class="form-group">
                      <select type="text" name="t1" class="form-control" id="dname" placeholder="Select Department">
                        
                      <?php 
                  
                    
                    $sql=("select Department_Name from department ");
                  $result=$conn->query($sql);
                  if($result->num_rows > 0)
                {
                  while($row = $result->fetch_assoc())
                {
                ?>
                        <option value="<?php echo $row["Department_Name"];?>" ><?php echo $row["Department_Name"]; ?> </option>
                        <?php
                      }
                  }
                
                
                ?>

                      </select>
                        </div>
                       </td>
                      <td>
                      <div class="form-group">
                      <input type="text" name="t2" class="form-control" id="pname" placeholder="Enter Program Name">
                        </div> 
                      </td>
                      <td>
                        <div class="form-group">
                      <input type="text" name="t3" class="form-control" id="pduration" placeholder="Enter Program Duration">
                        </div> 
                      </td>
                      <td>
                      <div class="form-group">
                      <input type="int" name="t4" class="form-control" id="sem" placeholder="Enter No Of Semesters">
                        </div> 
                      </td>
                      <td><div class="form-group">
                      <input type="int"  name="t5" class="form-control" id="fee" placeholder="Program Fee Per Sem">
                        </div> 
                      </td>
                      <td><div >
                    <button type="submit" name="submit" id="adddprogram" class="btn btn-primary">Add Program</button>
                  </div></td>
                   </tr>
                   </form>
                    
                  </table>
                </div><!-- /.box-body -->
              </div><!-- /.box -->
            </div>
          
          

             
           

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
                      <th></th>
                      
                    </tr>
                    <?php 
                    if(isset($_POST['submit']))
                    {
                    
                    $sql=("select *  from program order by id DESC");
                  $result=$conn->query($sql);
                  if($result->num_rows > 0)
                {
                  while($row = $result->fetch_assoc())
                {
                ?>
                    <tr>
                      <td><?php echo $row['Department_Name'] ;?></td>
                      <td><?php echo $row['Program_Name']; ?></td>
                      <td><?php echo $row['Program_Duration']; ?></td>
                      <td><?php echo $row['No_Of_Semester']; ?></td>
                      <td><?php echo $row['Fee']; ?></td>
                     
                   </tr>
                   <?php 
                   }
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
    </div>

          

    
                </div><!-- /.box-body -->
              </div><!-- /.box -->
            </div><!--/.col (right) -->
          </div>   <!-- /.row -->
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
    <!-- FastClick -->
    <script src='../../plugins/fastclick/fastclick.min.js'></script>
    <!-- AdminLTE App -->
    <script src="../../dist/js/app.min.js" type="text/javascript"></script>
    <!-- AdminLTE for demo purposes -->
    <script src="../../dist/js/demo.js" type="text/javascript"></script>
  </body>
</html>

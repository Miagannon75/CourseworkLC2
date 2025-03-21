<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Plotly Charts</title>
    <style>
      
      .topnav {
      overflow: hidden;
      background-color: #333;
        }

       /* Navbar links */
    .topnav a {
      float: left;
      display: block;
      color: #f2f2f2;
      text-align: center;
      padding: 14px 16px;
      text-decoration: none;
        }

    /* Links - change color on hover */
    .topnav a:hover {
      background-color: #ddd;
      color: black;
       }
    
    
      h1 { text-align: center; }
      
   </style>
</head>
<body>

    <div class="topnav">
        <a href="/">Home</a>
        <a href="/survey">Go to Survey Page</a>
    
    </div>

     <h1>Welcome to the Homepage!</h1>
    
    <h1>Charts</h1>

    <h2>Co.Donegal Bar Chart</h2>
    {{ bar_chart_donegal|safe }}
    
    <h2>Co.Dublin Bar Chart</h2>
    {{ bar_chart_dublin|safe }}
    
    <h2>Co.Galway Bar Chart</h2>
    {{ bar_chart_galway|safe }}
    
    <h2>Line Chart</h2>
    {{ line_chart|safe }}
    
    <h2>Scatter Plot</h2>
    {{ scatter_plot|safe }}
    
    <h2>Relationship Plot between Dublin and Galway</h2>
    {{ scatter_plot_2|safe}}
    
    
</body>
</html>
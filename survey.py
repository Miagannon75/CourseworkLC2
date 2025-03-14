<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page 2</title>
    
    
       <style>
          .topnav {
          overflow: hidden;
          background-color: #333;
            }
            
        .topnav a {
          float: left;
          display: block;
          color: #f2f2f2;
          text-align: center;
          padding: 14px 16px;
          text-decoration: none;
            }
        .topnav a:hover {
          background-color: #ddd;
          color: black;
           }
       
       
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 8px;
            border: 1px solid #ccc;
        }

        button {
            padding: 8px 12px;
            margin-right: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    
    <div class="topnav">
        <a href="/">Home</a>
    </div>
        
        
    <div class="container">
    <h1>Welcome to Page 2!</h1>

    <form id="suggestions-form">
        
        <label for="data">What data should be added to this website? (type a string)</label><br>
        <input type="text" id="data" required><br><br>
        
        <label for="year">What year should this data come from? (type an integer)</label><br>
        <input type="number" id="year" min="2000" max="2025" required><br><br>
        
        <label for="reliability">What should the reliability of this data be? (type a float)</label><br>
        <input type="number" id="reliability" step="0.1" min="1.0" max="10.0" required><br><br>
        
        <label for="opinion">Do you like this webpage?</label><br>
        <select id="opinion" required>
            <option value="">Select Boolean Value</option>
            <option value="Y">Yes</option>
            <option value="N">No</option>
        </select><br><br>
        
        <button type="button" onclick="saveData()">Submit</button>
        <button type="button" onclick="clearData()">Delete past data</button>
    </form>
    <br>
    <h2>Summary of submitted suggestions displayed</h2>
    
    <table id="data-table">
        <thead>
            <tr>
                <th>data</th>
                <th>year</th>
                <th>reliability</th>
                <th>opinion</th>
            </tr>
        </thead>
        
        <tbody>
        </tbody>
    </table>
    
    </div>
    
    <script>
    function saveData() {
        const data = document.getElementById('data').value;
        const year = document.getElementById('year').value;  // Fix: Changed 'date' to 'year' to match input ID
        const reliability = document.getElementById('reliability').value;  // Fix: Corrected the typo from 'reiability'
        const opinion = document.getElementById('opinion').value;  // Fix: Corrected the typo from 'permission'

        if (!data || !year || !reliability || !opinion) {
            alert("Please fill in all fields.");
            return;
        }

        const newData = { data, year, reliability, opinion };

        // Retrieve existing suggestions from localStorage, or initialize an empty array if none exists
        const suggestions = JSON.parse(localStorage.getItem('suggestions') || '[]');
        
        // Add the new suggestion to the array
        suggestions.push(newData);

        // Save the updated suggestions array back to localStorage
        localStorage.setItem('suggestions', JSON.stringify(suggestions));

        // Reload the table to display the updated suggestions
        loadTable();
    }

    function loadTable() {
        const tableBody = document.querySelector('#data-table tbody');  // Fix: Corrected the table body selector
        
        // Clear existing rows
        tableBody.innerHTML = '';

        // Retrieve suggestions from localStorage
        const suggestions = JSON.parse(localStorage.getItem('suggestions') || '[]');

        // Loop through each suggestion and add it as a row in the table
        suggestions.forEach(item => {
            const row = document.createElement('tr');  // Fix: Corrected 'document.creatELement' to 'document.createElement'

            row.innerHTML = `
                <td>${item.data}</td>
                <td>${item.year}</td>  <!-- Fix: Changed 'date' to 'year' to match object keys -->
                <td>${item.reliability}</td>
                <td>${item.opinion === 'Y' ? 'True' : 'False'}</td> <!-- Fix: Changed 'opionion' to 'opinion' -->
            `;

            // Append the row to the table body
            tableBody.appendChild(row);
        });
    }

    function clearData() {
        if (confirm("Are you sure you want to clear data?")) {
            localStorage.removeItem('suggestions');
            loadTable();
        }
    }

    // Load the table when the page is loaded
    document.addEventListener('DOMContentLoaded', loadTable);
    </script>

</body>
</html>
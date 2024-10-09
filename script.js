// Function to fetch and parse the CSV file
async function loadPlayers() {
    const response = await fetch('GW10_pred.csv');
    const data = await response.text();

    console.log("CSV Data Loaded: ", data); // Debugging: Check if CSV is being loaded
    
    const players = parseCSV(data);
    populateTable(players);
    setupSearch(players);
}


// Function to parse CSV into an array of player objects
function parseCSV(data) {
    const rows = data.split('\n');
    const players = [];

    rows.forEach((row, index) => {
        const columns = row.split(',');
        if (index !== 0 && columns[1] && columns[2]) {  // Ignore the first row (header)
            players.push({
                name: columns[1].trim(),
                prediction: columns[2].trim()
            });
        }
    });

    return players;
}

// Function to populate the table with player names and predictions
function populateTable(players) {
    const tableBody = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';  // Clear the table first to prevent duplication
    
    players.forEach(player => {
        const row = document.createElement('tr');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = player.name;
        row.appendChild(nameCell);
        
        const predictionCell = document.createElement('td');
        predictionCell.textContent = player.prediction;
        row.appendChild(predictionCell);
        
        tableBody.appendChild(row);
    });
}

// Function to setup the search inputs for filtering the table
function setupSearch(players) {
    document.getElementById('searchName').addEventListener('input', function() {
        const filteredPlayers = players.filter(player => 
            player.name.toLowerCase().includes(this.value.toLowerCase())
        );
        populateTable(filteredPlayers);
    });

    // document.getElementById('searchPrediction').addEventListener('input', function() {
    //     const filteredPlayers = players.filter(player => 
    //         player.prediction.toLowerCase().includes(this.value.toLowerCase())
    //     );
    //     populateTable(filteredPlayers);
    // });
}

// Call the function to load players when the page loads
window.onload = function() {
    loadPlayers();
};

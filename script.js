// script.js
// Function to fetch and parse the CSV file
async function loadPlayers() {
    const response = await fetch('players.csv');
    const data = await response.text();

    console.log("CSV Data Loaded: ", data); // Debugging: Check if CSV is being loaded
    
    const players = parseCSV(data);
    populateDropdown(players);
}


// Function to parse CSV into an array of player objects
function parseCSV(data) {
    const rows = data.split('\n');
    const players = [];

    rows.forEach(row => {
        const columns = row.split(',');
        if (columns[0] && columns[1] && columns[2]) {
            players.push({
                // index: columns[0].trim(),
                name: columns[1].trim(),
                prediction: columns[2].trim()
            });
        }
    });

    return players;
}

// Function to populate the dropdown with player names as plain text
function populateDropdown(players) {
    const playerDropdown = document.getElementById('playerDropdown');
    players.forEach(player => {
        const playerDiv = document.createElement('div');
        playerDiv.textContent = `${player.name} (${player.position}) - Points: ${player.prediction}`; // Display player name, position, and points
        playerDropdown.appendChild(playerDiv);
    });
}

// Function to toggle the player dropdown visibility
function toggleDropdown() {
    console.log("Dropdown Toggled"); // Debugging: Check if the button click is registered
    
    const playerDropdown = document.getElementById('playerDropdown');
    if (playerDropdown.style.display === "none" || playerDropdown.style.display === "") {
        playerDropdown.style.display = "block";
    } else {
        playerDropdown.style.display = "none";
    }
}

// Call the function to load players when the page loads
window.onload = function() {
    loadPlayers();
    
    // Add event listener to the "+" button to toggle the dropdown
    document.getElementById('togglePlayerDropdown').addEventListener('click', toggleDropdown);
};

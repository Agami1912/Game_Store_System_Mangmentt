document.addEventListener("DOMContentLoaded", function () {
    fetchGames();
    fetchCustomers();
    fetchLoanedGames();
});

function fetchGames() {
    fetch("/games")
        .then(response => response.json())
        .then(data => {
            let gameList = document.getElementById("game-list");
            gameList.innerHTML = "";
            let loanGameSelect = document.getElementById("loan-game-id");
            loanGameSelect.innerHTML = '<option value="">Select Game</option>';

            data.forEach(game => {
                gameList.innerHTML += `
                    <p>${game.title} - ${game.genre} - $${game.price}
                    <b>(Quantity: ${game.quantity})</b>
                    <button class="delete-game-btn" data-game-id="${game.id}"> Delete</button>
                    </p>`;

                if (game.quantity > 0) {
                    loanGameSelect.innerHTML += `<option value="${game.id}">${game.title} (Qty: ${game.quantity})</option>`;
                }
            });

            document.querySelectorAll(".delete-game-btn").forEach(button => {
                button.addEventListener("click", function() {
                    deleteGame(this.dataset.gameId);
                });
            });

        })
        .catch(error => console.error("Error fetching games:", error));
}

function fetchCustomers() {
    fetch("/customers/")
        .then(response => response.json())
        .then(data => {
            let customerList = document.getElementById("customer-list");
            customerList.innerHTML = "";
            let loanCustomerSelect = document.getElementById("loan-customer-id");
            loanCustomerSelect.innerHTML = '<option value="">Select Customer</option>';

            data.forEach(customer => {
                customerList.innerHTML += `
                    <p>${customer.name} - ${customer.email}
                    <button class="delete-customer-btn" data-customer-id="${customer.id}"> Delete</button>
                    </p>`;

                loanCustomerSelect.innerHTML += `<option value="${customer.id}">${customer.name}</option>`;
            });

            document.querySelectorAll(".delete-customer-btn").forEach(button => {
                button.addEventListener("click", function () {
                    deleteCustomer(this.dataset.customerId);
                });
            });
        })
        .catch(error => console.error("Error fetching customers:", error));
}
function fetchLoanedGames() {
    fetch("/loans/")
        .then(response => response.json())
        .then(data => {
            let loanedGamesList = document.getElementById("loaned-games-list");
            loanedGamesList.innerHTML = "";

            data.forEach(loan => {
                loanedGamesList.innerHTML += `
                    <p>${loan.title} - Loaned to ${loan.customer}
                    <button onclick="returnGame(${loan.id})"> Return</button>
                    </p>`;
            });
        })
        .catch(error => console.error("Error fetching loaned games:", error));
}



function loanGame() {
    let gameId = document.getElementById("loan-game-id").value;
    let customerId = document.getElementById("loan-customer-id").value;

    fetch("/loans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, customer_id: customerId })
    })
    .then(response => response.json())
    .then(() => {
        fetchGames();
        fetchLoanedGames();
        hideLoanGameForm();
    })
    .catch(error => console.error("Error loaning game:", error));
}


function returnGame(gameId) {
    fetch(`/loans/${gameId}`, { method: "DELETE" })
    .then(() => {
        fetchGames();
        fetchLoanedGames();
    })
    .catch(error => console.error("Error returning game:", error));
}
function addGame()      {
    let title = document.getElementById("game-title").value;
    let genre = document.getElementById("game-genre").value;
    let price = document.getElementById("game-price").value;
    let quantity = document.getElementById("game-quantity").value;

    fetch("/games"  , {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, genre, price, quantity })
    })
    .then(response => response.json())
    .then(() => {
        fetchGames();
        hideAddGameForm();
    })
    .catch(error => console.error("Error adding game:", error));
}

function deleteGame(gameId) {
    fetch(`/games/games/${gameId}`, { method: "DELETE" })
        .then(() => fetchGames())
        .catch(error => console.error("Error deleting game:", error));
}

function addCustomer() {
    let name = document.getElementById("customer-name").value;
    let email = document.getElementById("customer-email").value;
    let phone = document.getElementById("customer-phone").value;

    fetch("/customers/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, phone })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(() => {
        fetchCustomers();
        hideAddCustomerForm();
    })
    .catch(error => console.error("Error adding customer:", error));
}


function deleteCustomer(customerId) {
    fetch(`/customers/customers/${customerId}`, { method: "DELETE" })
        .then(() => fetchCustomers())
        .catch(error => console.error("Error deleting customer:", error));
}

function showAddGameForm() {
    document.getElementById("add-game-form").style.display = "block";
}

function hideAddGameForm() {
    document.getElementById("add-game-form").style.display = "none";
}
function showLoanGameForm() {
    document.getElementById("loan-game-form").style.display = "block";
}
function hideLoanGameForm() {
    document.getElementById("loan-game-form").style.display = "none";
}

function showAddCustomerForm() {
    document.getElementById("add-customer-form").style.display = "block";
}
function hideAddCustomerForm() {
    document.getElementById("add-customer-form").style.display = "none";
}
function logout() {
    fetch("/logout", {
        method: "GET"
    })
    .then(() => window.location.href = "/login") // ✅ Redirect to login
    .catch(error => console.error("Error logging out:", error));
}
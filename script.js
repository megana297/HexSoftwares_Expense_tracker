function addExpense() {
    const category = document.getElementById("category").value;
    const amount = document.getElementById("amount").value;
    const description = document.getElementById("description").value;

    if (!category || !amount) {
        alert("Please enter category and amount");
        return;
    }

    fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            category: category,
            amount: amount,
            description: description
        })
    })
    .then(response => response.json())
    .then(() => {
        loadExpenses();
        document.getElementById("category").value = "";
        document.getElementById("amount").value = "";
        document.getElementById("description").value = "";
    });
}

function loadExpenses() {
    fetch("/expenses")
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("expense-list");
            table.innerHTML = "";

            data.forEach(expense => {
                table.innerHTML += `
                    <tr>
                        <td>${expense.category}</td>
                        <td>₹${expense.amount}</td>
                        <td>${expense.description || ""}</td>
                    </tr>
                `;
            });
        });
}

loadExpenses();

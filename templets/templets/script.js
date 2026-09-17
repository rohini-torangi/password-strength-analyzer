console.log("Password Security Analyzer loaded successfully.");

const passwordInput = document.getElementById("password");

if (passwordInput) {
    passwordInput.addEventListener("input", function () {
        console.log("Password entered for analysis.");
    });
}

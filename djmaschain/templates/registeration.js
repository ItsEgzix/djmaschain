function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    // Example credentials
    const validEmail = "test@example.com";
    const validPassword = "password123";

    if (email === validEmail && password === validPassword) {
        alert("Login successful!");
        // Redirect to another page or perform any action you want
        window.location.href = "index.html";
    } else {
        alert("Invalid email or password. Please try again.");
    }
}

function signUp() {
    // Add your sign-up logic here if needed
    alert("Sign up functionality is not implemented yet.");
}
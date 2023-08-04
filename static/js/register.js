// function validation() {
//     // Form validation logic here
//     const form = document.forms.Formfill;
//     const username = form.username.value;
//     const email = form.email.value;
//     const password = form.password.value;
//     const cPassword = form.cPassword.value;

//     // Add your form validation code here (e.g., check if the fields are not empty, match passwords, etc.)

//     // If the form is valid, submit the data using AJAX
//     const xhr = new XMLHttpRequest();
//     xhr.open("POST", "/register", true);
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 const response = JSON.parse(xhr.responseText);
//                 if (response.success) {
//                     // Show the success popup
//                     document.getElementById("popup").style.display = "block";
//                 } else {
//                     // Handle other possible errors (e.g., invalid user, invalid password)
//                     alert(response.error);
//                 }
//             } else {
//                 // Handle server error
//                 alert("Server Error: Please try again later.");
//             }
//         }
//     };

//     const data = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
//     xhr.send(data);

//     // Prevent the form from submitting normally
//     return false;
// }

// function closeSlide() {
//     // Hide the success popup and reset the form
//     document.getElementById("popup").style.display = "none";
//     document.forms.Formfill.reset();
// }
// function validation() {
//     // Form validation logic here
//     const form = document.forms.Formfill;
//     const username = form.username.value;
//     const password = form.password.value;

//     // Add your form validation code here (e.g., check if the fields are not empty, etc.)
//     // You can also implement more comprehensive validation, such as matching password requirements.

//     // If the form is valid, submit the data using AJAX
//     const xhr = new XMLHttpRequest();
//     xhr.open("POST", "/register", true);
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 const response = JSON.parse(xhr.responseText);
//                 if (response.success) {
//                     // Show the success popup
//                     document.getElementById("popup").style.display = "block";
//                 } else {
//                     // Handle other possible errors (e.g., invalid user, invalid password)
//                     alert(response.error);
//                 }
//             } else {
//                 // Handle server error
//                 alert("Server Error: Please try again later.");
//             }
//         }
//     };

//     const data = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
//     xhr.send(data);

//     // Prevent the form from submitting normally
//     return false;
// }

// function closeSlide() {
//     // Hide the success popup and reset the form
//     document.getElementById("popup").style.display = "none";
//     document.forms.Formfill.reset();
// }
document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.getElementById("registration-form");
    const messageDiv = document.getElementById("message");

    registrationForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(registrationForm);
        const data = {
            username: formData.get("username"),
            password: formData.get("password"),
        };

        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((result) => {
            if (result.success) {
                // Registration successful, show success message
                messageDiv.innerHTML = `<p style="color: green;">${result.success}</p>`;
            } else if (result.error) {
                // Registration failed, show error message
                messageDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
            }
        })
        .catch((error) => {
            // Fetch or server-related error, show error message
            messageDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again later.</p>`;
            // console.error(error);
        });
    });
});

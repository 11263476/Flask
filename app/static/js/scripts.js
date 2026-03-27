// Function to handle student deletion asynchronously
async function deleteStudent(id) {
    // Show a browser confirmation dialog to prevent accidental clicks
    if (confirm('Are you sure you want to delete this student record?')) {
        try {
            // Send a DELETE request to our API endpoint
            const response = await fetch(`/api/students/${id}`, {
                method: 'DELETE', // Specify the HTTP method
            });

            // If the server returns a success (200) status
            if (response.ok) {
                // Refresh the page to show the updated list
                window.location.reload();
            } else {
                // Alert the user if the server returned an error (like 404)
                alert('Error: Could not delete student.');
            }
        } catch (error) {
            // Handle network errors or other unexpected issues
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        }
    }
}

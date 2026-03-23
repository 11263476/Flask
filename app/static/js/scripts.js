async function deleteStudent(studentId) {
    if (!confirm('Are you sure you want to delete this student?')) {
        return;
    }

    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error deleting student');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
}

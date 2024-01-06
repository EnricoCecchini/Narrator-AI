import { API_ROUTE } from "./api";

export function upload_file(new_file) {
    console.log(new_file)

    return fetch(API_ROUTE + '/upload_file', {
        method: 'POST',
        body: new_file,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Form submitted:', data);
        // Handle the response as needed
    })
    .catch(error => {
        console.error('Error submitting form:', error);
    });
}
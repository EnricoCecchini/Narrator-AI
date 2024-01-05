import { API_ROUTE } from "./api";

export function upload_book(new_book) {
    console.log(new_book)

    return fetch(API_ROUTE + '/upload_book', {
        method: 'POST',
        body: new_book,
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

export function upload_speaker(new_speaker) {
    console.log(new_speaker)

    return fetch(API_ROUTE + '/upload_book', {
        method: 'POST',
        body: new_speaker,
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

export function upload_rvc(new_RVC) {
    console.log(new_RVC)

    return fetch(API_ROUTE + '/upload_book', {
        method: 'POST',
        body: new_RVC,
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
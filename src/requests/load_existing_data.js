import { API_ROUTE } from "./api";

export function load_existing_files() {
    // Fetch from API/load_existing_items

    fetch(API_ROUTE + '/load_existing_items', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        localStorage.setItem('existing_books', JSON.stringify(data.books))
        localStorage.setItem('existing_speakers', JSON.stringify(data.speakers))
        localStorage.setItem('existing_rvc', JSON.stringify(data.rvc_models))
        localStorage.setItem('existing_audiobooks', JSON.stringify(data.audiobooks))
    })
    .catch(e => {
        console.log(e)
    })
}
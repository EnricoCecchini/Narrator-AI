import { API_ROUTE } from "./api";

export const narrate_missing_lines = async (book_data) => {
    console.log('BOOK: ', book_data)

    return fetch(API_ROUTE + '/narrate_missing_lines', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(book_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        alert(data.message)
        return data
    })
    .catch(e => {
        console.log(e)
    })
}
import { API_ROUTE } from "./api";

export const save_book_changes = async (book_data) => {
    console.log('CHANGES: ', book_data)

    return fetch(API_ROUTE + '/save_book_changes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(book_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        return data
    })
    .catch(e => {
        console.log(e)
    })
}
import { API_ROUTE } from "./api";

export const load_book = async (book) => {
    const response = await fetch(API_ROUTE + `/load_selected_book?selected_book=${book}`)
    const book_content = await response.json()

    //console.log(book_content)

    return book_content
}
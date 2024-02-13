import { API_ROUTE } from "./api";
import {existing_books, existing_speakers, existing_rvc, existing_rvc_index, existing_audiobooks} from '../../static/store'


export const load_existing_files = async() => {
    // Fetch from API/load_existing_items

    try {
        const resp = await fetch(API_ROUTE + '/load_existing_items', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })

        if (!resp.ok) {
            throw new Error('Failed to fetch existing files')
        }

        const data = await resp.json()
        console.log(data)


        existing_books.set(JSON.stringify(data.books))
        existing_speakers.set(JSON.stringify(data.speakers))
        existing_rvc.set(JSON.stringify(data.rvc_models))
        existing_rvc_index.set(JSON.stringify(data.indexes))
        existing_audiobooks.set(JSON.stringify(data.audiobooks))


        // await localStorage.setItem('existing_books', JSON.stringify(data.books))
        // await localStorage.setItem('existing_speakers', JSON.stringify(data.speakers))
        // await localStorage.setItem('existing_rvc', JSON.stringify(data.rvc_models))
        // await localStorage.setItem('existing_rvc_index', JSON.stringify(data.indexes))
        // await localStorage.setItem('existing_audiobooks', JSON.stringify(data.audiobooks))



    } catch (e) {
        console.log(e)
    }

    // await fetch(API_ROUTE + '/load_existing_items', {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     }
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log(data)
    //     localStorage.setItem('existing_books', JSON.stringify(data.books))
    //     localStorage.setItem('existing_speakers', JSON.stringify(data.speakers))
    //     localStorage.setItem('existing_rvc', JSON.stringify(data.rvc_models))
    //     localStorage.setItem('existing_rvc_index', JSON.stringify(data.indexes))
    //     localStorage.setItem('existing_audiobooks', JSON.stringify(data.audiobooks))
    // })
    // .catch(e => {
    //     console.log(e)
    // })
}
import {writable} from 'svelte/store'

export const existing_books = writable(localStorage.getItem('existing_books'))
export const existing_speakers = writable(localStorage.getItem('existing_speakers'))
export const existing_rvc = writable(localStorage.getItem('existing_rvc'))
export const existing_audiobooks = writable(localStorage.getItem('existing_audiobooks'))

export const selected_book = writable('')
export const selected_speaker = writable('')
export const selected_rvc = writable('')
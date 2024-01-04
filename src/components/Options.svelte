<script>
    import { onMount } from 'svelte';
    import {writable} from 'svelte/store';

    import {load_existing_files} from '../requests/load_existing_data'
    import {upload_book} from '../requests/upload_book'

    import {existing_books, existing_speakers, existing_rvc} from '../../static/store'
    import {selected_book, selected_speaker, selected_rvc} from '../../static/store'

    let available_books = []
    let available_speakers = []
    let available_rvc = []
    let available_audiobooks = []

    let selected_book_option = ''
    let selected_speaker_option = ''
    let selected_rvc_option = ''

    onMount(async () => {
        load_existing_files()
        console.log('BOOKS EXISTING: ', $existing_books)
        handleParseOptions()
        loadSelectedStore()
    })
    
    const loadSelectedStore = async () => {
        selected_book.subscribe(value => {
            selected_book_option = value
        })

        selected_speaker.subscribe(value => {
            selected_speaker_option = value
        })

        selected_rvc.subscribe(value => {
            selected_rvc_option = value
        })
    }

    const handleParseOptions = () => {
        available_books = JSON.parse($existing_books)
        console.log("PARSED BOOKS", available_books)
        
        available_speakers = JSON.parse($existing_speakers)
        available_rvc = JSON.parse($existing_rvc)
        available_audiobooks = []   
    }

    

    const handleUploadBook = async (event) => {
        event.preventDefault()

        // Make form data to POST
        const new_book = new FormData(event.target)

        if (new_book) {
            console.log('BOOK NAME', new_book)
            const response = await upload_book(new_book)
        } else {
            console.log("NO BOOK UPLOADED")
        }

        load_existing_files()
        handleParseOptions()
    }

    const handleSelectBook = (event) => {
        console.log(event.target.value)
        selected_book.set(event.target.value)
    }

    const handleSelectSpeaker = (event) => {
        console.log(event.target.value)
        selected_speaker.set(event.target.value)
    }

    const handleSelectRVC = (event) => {
        console.log(event.target.value)
        selected_rvc.set(event.target.value)
    }

</script>

<div class="container">
    <div class="options-row">
        <!-- Select Book -->
        <div class="options-column">
            <div class="options-col-row">
                <label for="books" class="option-label">Select a book</label>
            </div>
            <div class="options-col-row">
                <select class="option-dropdown" name='books' id='books' on:change={handleSelectBook}>
                    <option value='' class="options-option">Select a book</option>
                    {#each available_books as book}
                        <option value={book}>{book}</option>
                    {/each}
                </select>
            </div>
        </div>

        <!-- Select Speaker -->
        <div class="options-column">
            <div class="options-col-row">
                <label for="speakers" class="option-label">Select speaker</label>
            </div>
            <div class="options-col-row">
                <select class="option-dropdown" name='speakers' id='speakers'  on:change={handleSelectSpeaker}>
                    <option value='' class="options-option">Select a Speaker</option>
                    {#each available_speakers as speaker}
                        <option value={speaker}>{speaker}</option>
                    {/each}
                </select>
            </div>
        </div>

        <!-- Select RVC Model -->
        <div class="options-column">
            <div class="options-col-row">
                <label for="speakers" class="option-label">Select RVC</label>
            </div>
            <div class="options-col-row">
                <select class="option-dropdown" name='speakers' id='speakers'  on:change={handleSelectRVC}>
                    <option value='' class="options-option">Select RVC</option>
                    {#each available_rvc as rvc}
                        <option value={rvc}>{rvc}</option>
                    {/each}
                </select>
            </div>
        </div>

        <!-- Upload Book -->
        <div class="options-column">
            <form on:submit|preventDefault={handleUploadBook}>
                <div class="options-col-row">
                    <label for="upload_book" class="option-label">Upload Book</label>
                </div>
                <div class="options-col-row">
                    <input class="upload_book" type="file" accept=".txt" name="upload_book" id="upload_book">
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
    @import 'src/app.css';
</style>
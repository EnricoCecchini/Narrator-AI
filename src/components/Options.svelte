<script>
    import { onMount } from 'svelte';
    import {writable} from 'svelte/store';

    import { API_ROUTE } from "../requests/api";

    import {load_existing_files} from '../requests/load_existing_data'
    import {upload_file} from '../requests/upload_files'
    import {load_book} from '../requests/load_book'

    import {existing_books, existing_speakers, existing_rvc} from '../../static/store'
    import {selected_book, selected_speaker, selected_rvc} from '../../static/store'
    import {selected_book_lines} from '../../static/store'

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

    const handleUploadFile = async (event) => {
        event.preventDefault()

        // Make form data to POST
        const new_file = new FormData(event.target)

        if (new_file) {
            console.log('FILE NAME', new_file)
            const response = await upload_file(new_file)
        } else {
            console.log("NO FILE UPLOADED")
        }

        loadSelectedStore()
        handleParseOptions()
    }

    const handleSelectBook = async (event) => {
        console.log(event.target.value)
        selected_book.set(event.target.value)

        const response = await load_book(event.target.value)

        // Save lines from selected book in store
        selected_book_lines.set(response.data)
    }

    const handleSelectSpeaker = async (event) => {
        console.log(event.target.value)

        // Set selected speaker in store
        selected_speaker.set(event.target.value)
    }

    const handleSelectRVC = async (event) => {
        console.log(event.target.value)

        // Set selected RVC in store
        selected_rvc.set(event.target.value)
    }

</script>

<div class="options-container">
    <div class="options-group-narrator">
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
        </div>
    </div>

    <div class="options-group-upload">
        <!-- Upload Book -->
        <div class="options-column">
            <form on:submit|preventDefault={handleUploadFile}>
            <!-- <form on:submit|preventDefault={handleUploadBook}> -->
                <div class="options-col-row">
                    <label for="upload_file" class="option-label">Upload Book</label>
                </div>
                <div class="options-col-row">
                    <!-- <input class="upload_file" type="file" accept=".txt" name="upload_book" id="upload_book"> -->
                    <input class="upload_file" type="file" accept=".txt" name="upload_file" id="upload_file">
                    <button type="submit">Submit</button>
                </div>
            </form>

            <form on:submit|preventDefault={handleUploadFile}>
                <div class="options-col-row">
                    <label for="upload_file" class="option-label">Upload Speaker</label>
                </div>
                <div class="options-col-row">
                    <!-- <input class="upload_file" type="file" accept=".wav" name="upload_speaker" id="upload_speaker"> -->
                    <input class="upload_file" type="file" accept=".wav" name="upload_file" id="upload_file">
                    <button type="submit">Submit</button>
                </div>
            </form>

            <form on:submit|preventDefault={handleUploadFile}>
                <div class="options-col-row">
                    <label for="upload_file" class="option-label">Upload RVC</label>
                </div>
                <div class="options-col-row">
                    <!-- <input class="upload_file" type="file" accept=".txt" name="upload_RVC" id="upload_RVC"> -->
                    <input class="upload_file" type="file" accept=".txt" name="upload_file" id="upload_file">
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
    @import 'src/app.css';
</style>
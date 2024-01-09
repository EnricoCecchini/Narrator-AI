<script>
    import { onDestroy } from 'svelte';

    import {    selected_book_lines,
                selected_book,
                selected_speaker,
                selected_rvc
    } from '../../static/store'

    import { narrate_line } from '../requests/narrate_line'

    let book_lines = []

    const unsubscribeSelectedLines = selected_book_lines.subscribe(value => {
        book_lines = value
    })

    const handleNarrateLine = async (line, index) => {
        const data = {
            line: line,
            index: index,
            book: $selected_book,
            speaker: $selected_speaker,
            rvc_model: $selected_rvc
        }

        console.log(data)
        const audio = await narrate_line(data)
    }

    onDestroy(() => {
        unsubscribeSelectedLines()
    })

</script>

<div class="book-container">
    <table class="book-table">
        <tr class="book-table-header-row">
            <td class="book-table-header-number">#</td>
            <td class="book-table-header-line">Line</td>
            <td class="book-table-header-options">Options</td>
        </tr>
        {#each book_lines as line, i}
            <tr class="book-table-row">
                <td class="book-table-line-number">{i+1}</td>
                <td>
                    <textarea class="book-table-text" value={line} />
                </td>
                <td>
                    <button class="book-button" on:click={handleNarrateLine(line, i)}>Regenerate</button>
                    <button class="book-button">Play</button>
                    <button class="book-button">Delete</button>
                </td>
            </tr>
        {/each}
    </table>

</div>
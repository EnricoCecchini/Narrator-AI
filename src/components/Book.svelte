<script>
    import { onDestroy } from 'svelte';
    import {selected_book_lines} from '../../static/store'

    let book_lines = []

    const unsubscribe = selected_book_lines.subscribe(value => {
        book_lines = value
    })

    onDestroy(() => {
        unsubscribe()
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
                    <button class="book-button">Regenerate</button>
                    <button class="book-button">Play</button>
                    <button class="book-button">Delete</button>
                </td>
            </tr>
        {/each}
    </table>

</div>
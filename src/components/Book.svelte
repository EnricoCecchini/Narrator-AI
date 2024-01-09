<script>
    import { onDestroy } from 'svelte';

    import {    selected_book_lines,
                selected_book,
                selected_speaker,
                selected_rvc
    } from '../../static/store'

    import { narrate_line } from '../requests/narrate_line'
    import {load_book} from '../requests/load_book'

    let book_lines = []

    const unsubscribeSelectedLines = selected_book_lines.subscribe(value => {
        book_lines = value
    })

    // Narrate selected line
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

    // Delete selected line
    const handleDeleteLine = async (index) => {
        const data = {
            index: index,
            book: $selected_book,
        }

        book_lines.splice(index, 1)

        selected_book_lines.set(book_lines)

        // Delete line from book_lines
        console.log('DELETE: ', data)
    }

    // Play selected line
    const handlePlayLine = async (index) => {
        const data = {
            index: index,
            book: $selected_book,
        }

        console.log('PLAY: ', data)
    }

    // Add line below selected line
    const handleAddLineBelow = async (index) => {
        book_lines.splice(index + 1, 0, '')

        selected_book_lines.set(book_lines)
    }

    const handleMoveLineUp = async (index) => {
        let tempLine = book_lines[index]

        book_lines[index] = book_lines[index - 1]
        book_lines[index - 1] = tempLine

        selected_book_lines.set(book_lines)
    }

    const handleMoveLineDown = async (index) => {
        let tempLine = book_lines[index]

        book_lines[index] = book_lines[index + 1]
        book_lines[index + 1] = tempLine

        selected_book_lines.set(book_lines)
    }

    const handleUndoChanges = async () => {
        console.log('UNDO: ', $selected_book)
        //selected_book.set(event.target.value)

        const response = await load_book($selected_book)

        // Save lines from selected book in store
        selected_book_lines.set(response.data)
    }

    onDestroy(() => {
        unsubscribeSelectedLines()
    })

</script>

<div class="book-container">
    <div class="book-content">
        <table class="book-table">
            <tr class="book-table-header-row">
                <td class="book-table-header-number">#</td>
                <td class="book-table-header-line">Line</td>
                <td class="book-table-header-options">Options</td>
                <td class="book-table-header-move">Move</td>
            </tr>
            {#each book_lines as line, i}
                <tr class="book-table-row">
                    <td class="book-table-line-number">{i}</td>
                    <td>
                        <textarea class="book-table-text" value={line} />
                    </td>
                    <td>
                        <button class="book-line-button" on:click={() => handleNarrateLine(line, i)}>Narrate Line</button>
                        <button class="book-line-button" on:click={() => handlePlayLine(i)}>Play Line</button>
                        <button class="book-line-button" on:click={() => handleAddLineBelow(i)}>Add Line Below</button>
                        <button class="book-line-button delete" on:click={() => handleDeleteLine(i)}>Delete Line</button>
                    </td>
                    <td>
                        {#if i > 0}
                            <button class="book-line-button-move" on:click={() => {handleMoveLineUp(i)}}>↑</button>
                        {/if}
                        {#if i < book_lines.length - 1}
                            <button class="book-line-button-move" on:click={() => {handleMoveLineDown(i)}}>↓</button>
                        {/if}
                    </td>
                </tr>
            {/each}
        </table>
    </div>
    <div class="book-options">
        <button class="book-options-button">Narrate All</button>
        <button class="book-options-button">Play All</button>
        <button class="book-options-button">Pause</button>
        <button class="book-options-button restore" on:click={handleUndoChanges}>Undo Changes</button>
        <button class="book-options-button save">Save Changes</button>
    </div>
</div>
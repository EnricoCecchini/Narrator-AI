<script>
    import { onDestroy, onMount } from 'svelte';

    import {
        selected_book_lines,
        selected_book,
        selected_speaker,
        selected_rvc,
        selected_index,
        AUDIO_PATH,
    } from '../../static/store'

    import { narrate_line } from '../requests/narrate_line'
    import { load_book } from '../requests/load_book'
    import { save_book_changes } from '../requests/save_book_changes'
    import { narrate_book } from '../requests/narrate_book'
    import { pause_narration } from '../requests/pause_narration'
    import { check_audio_exists } from '../requests/check_audio_exists'
    import { merge_book, check_narrated_lines } from '../requests/merge_book'
    import { narrate_missing_lines } from '../requests/narrate_missing_lines'


    let book_lines = []
    let audioList = []

    let audio = null
    let mergedAudio = null
    let currentAudioIndex = 0
    let isPaused = true

    let index_effect = 0
    let voice_pitch = 0


    const unsubscribeSelectedLines = selected_book_lines.subscribe(value => {
        book_lines = value
        console.log('BOOK LINES: ', book_lines)
    })


    // Delete selected line
    const handleDeleteLine = async (index) => {
        book_lines.splice(index, 1)
        selected_book_lines.set(book_lines)
    }


    // Add line below selected line
    const handleAddLineBelow = async (index) => {
        book_lines.splice(index + 1, 0, {'line': '', 'path': ''})
        selected_book_lines.set(book_lines)
    }


    // Move selected line up
    const handleMoveLineUp = async (index) => {
        let tempLine = book_lines[index]

        book_lines[index] = book_lines[index - 1]
        book_lines[index - 1] = tempLine

        selected_book_lines.set(book_lines)
        console.log('BOOK LINES: ', book_lines)
        //audioList = new Array(book_lines.length)
        console.log('AUDIO LIST: ', audioList)
    }


    // Move selected line down
    const handleMoveLineDown = async (index) => {
        let tempLine = book_lines[index]

        book_lines[index] = book_lines[index + 1]
        book_lines[index + 1] = tempLine

        selected_book_lines.set(book_lines)
        //audioList = new Array(book_lines.length)
        console.log('AUDIO LIST: ', audioList)
    }


    // Begin Book Narration
    const handleMissingLines = async () => {

        let resp = await handleSaveChanges()

        console.log('RESP', resp)

        if (!resp.success) {
            alert('Please save changes before narrating book')

            return
        }

        const data = {
            book: $selected_book,
            speaker: $selected_speaker,
            rvc_model: $selected_rvc,
            index: $selected_index,
            rvc_index: $selected_index,
            index_effect: index_effect / 100,
            voice_pitch: voice_pitch
        }

        console.log('BEGIN NARRATION: ', data)

        const response = await narrate_missing_lines(data)

        await handleReloadBook()
    }


    // Begin Book Narration
    const handleNarrateBook = async () => {

        let resp = await handleSaveChanges()

        console.log('RESP', resp)

        if (!resp.success) {
            alert('Please save changes before narrating book')

            return
        }

        const data = {
            book: $selected_book,
            speaker: $selected_speaker,
            rvc_model: $selected_rvc,
            index: $selected_index,
            rvc_index: $selected_index,
            index_effect: index_effect / 100,
            voice_pitch: voice_pitch
        }

        console.log('BEGIN NARRATION: ', data)

        const response = await narrate_book(data)

        await handleReloadBook()
    }


    // Narrate selected line
    const handleNarrateLine = async (line, index) => {
        await handleSaveChanges()

        const data = {
            line: line,
            index: index,
            book: $selected_book,
            speaker: $selected_speaker,
            rvc_model: $selected_rvc,
            rvc_index: $selected_index,
            index_effect: index_effect / 100,
            voice_pitch: voice_pitch
        }

        if (data.speaker === '') {
            alert('Please select a speaker')
            return
        }

        alert('Narrating Line')
        console.log(data)

        await narrate_line(data)
        await handleReloadBook()
    }


    // Pause Book Narration
    const handlePauseNarration = async () => {
        console.log('PAUSE NARRATION')

        const response = await pause_narration()
    }


    // Save changes to book
    const handleSaveChanges = async () => {
        const data = {
            book: $selected_book,
            lines: book_lines
        }

        const response = await save_book_changes(data)

        await handleReloadBook()

        await handleReloadAudios()

        console.log('CHANGE RESPONSE: ', response)

        return response
    }


    const handleReloadAudios = async () => {
        const newAudioList = []

        for (let i = 0; i < book_lines.length; i++) {
            let audio_path = `${AUDIO_PATH}\\${$selected_book}\\${i}.wav`
            console.log('AUDIO PATH: ', audio_path)

            // Check if audio file exists
            const audio_exists = await check_audio_exists(audio_path)

            console.log('AUDIO EXISTS: ', audio_exists)

            if (audio_exists) {
                console.log('AUDIO EXISTS: ', audio_path)

                // Load audio file into audio list using fetch
                await fetch(audio_path)
                    .then(response => response.blob())
                    .then(blob => {
                        const audio = new Audio(URL.createObjectURL(blob))
                        newAudioList.push(audio)
                    })

            } else {
                console.log('AUDIO DOES NOT EXIST: ', audio_path)
                newAudioList.push(null)
            }

            console.log('AUDIO LIST: ', audioList)
        }

        // Empty audio list
        audioList = new Array(book_lines.length)

        audioList = newAudioList
    }


    // Undo unsaved changes by reloading lines from selected book
    const handleReloadBook = async () => {
        const response = await load_book($selected_book)

        // Save lines from selected book in store
        selected_book_lines.set(response.data)

        //audioList = new Array(book_lines.length)
        console.log('AUDIO LIST RELOAD: ', audioList)

        audioList = []

        await handleReloadAudios()
    }


    // Merge generated audios in single audiobook
    const handleMergeBook = async () => {
        const data = {
            book: $selected_book,
            speaker: $selected_speaker,
            rvc_model: $selected_rvc,
            index: $selected_index
        }

        await handleSaveChanges()

        // Check all lines are narrated
        const narrated_lines = await check_narrated_lines(data)

        console.log('NARRATED LINES: ', narrated_lines)

        if (!narrated_lines.success) {
            alert('Please narrate all lines before merging book')

            return
        }

        const response = await merge_book(data)
    }


    const handlePlayLine = async (index) => {
        // Pause audio if playing
        await handlePausePlaying()

        isPaused = false

        console.log('AUDIO SOURCE: ', `${AUDIO_PATH}\\${$selected_book}\\${index}.wav`)
        audio = audioList[index]

        try {
            audio.currentTime = 0
        } catch(e) {
            alert('Line has not been narrated yet')
            return
        }

        console.log('AUDIO: ', audio)
        console.log('AUDIO LIST PLAY: ', audioList)

        try {
            // If not playing, play audio
            if (audio) {
                // Reset audio to beginning
                audio.currentTime = 0

                // Use await to ensure playback completes before moving on
                await audio.play()
            } else {
                // If playing, pause audio
                audio.pause()
            }
        } catch (e) {
            console.log('ERROR PLAYING LINE: ', e)
            alert('ERROR PLAYING LINE: ' + e)
        }
    }

    const handlePlayMerged = async () => {
        // Pause audio if playing
        await handlePausePlaying()

        isPaused = false

        const merged_audio_path = `${AUDIO_PATH}\\${$selected_book}\\audiobook\\audiobook.wav`

        console.log('MERGED AUDIO PATH: ', merged_audio_path)

        // Check if audio file exists
        const audio_exists = await check_audio_exists(merged_audio_path)

        console.log('AUDIO EXISTS: ', audio_exists)

        if (audio_exists && !isPaused) {
            console.log('AUDIO EXISTS: ', merged_audio_path)

            // Load audio file into audio list using fetch
            await fetch(merged_audio_path)
                .then(response => response.blob())
                .then(async blob => {
                    mergedAudio = new Audio(URL.createObjectURL(blob))
                    // Use await to ensure playback completes before moving on
                    await mergedAudio.play()
                })
        }
    }

    const playNextLine = async () => {
        console.log('PLAY NEXT LINE: ', currentAudioIndex)
        console.log('AUDIO LIST PLAYING: ', audioList)

        if (currentAudioIndex < audioList.length && !isPaused) {
            audio = audioList[currentAudioIndex]

            if (audio) {
                // Use await to ensure playback completes before moving on
                await audio.pause()
                audio.currentTime = 0
            }

            console.log('CURRENT AUDIO: ', audio)

            try {
                if (audio !== null) {
                    // Use await to ensure playback completes before moving on
                    await audio.play()

                    const endedCallback = async () => {
                        console.log('AUDIO ENDED')
                        audio.removeEventListener('ended', endedCallback)
                        currentAudioIndex += 1
                        await playNextLine()
                    }

                    audio.addEventListener('ended', endedCallback)
                } else {
                    currentAudioIndex += 1
                    await playNextLine()
                }
            } catch (e) {
                console.log('ERROR PLAYING LINE: ', e)

                if (e instanceof DOMException) {
                    console.log('ERROR PLAYING LINE: ' + e)
                } else {
                    console.log('ERROR PLAYING LINE: ', e)
                }
            }
        }
    }

    const handlePlayAll = async () => {
        console.log('PLAY ALL')

        // Pause audio if playing
        await handlePausePlaying()

        audio = audioList[0]
        audio.currentTime = 0

        isPaused = false
        currentAudioIndex = 0
        // Use await to ensure playback completes before moving on
        await playNextLine()
    }

    // Pause playing all audio
    const handlePausePlaying = async () => {
        if (audio) {
            // Use await to ensure playback completes before moving on
            await audio.pause()
            audio.currentTime = 0
        }

        audio = audioList[0]
        audio.currentTime = 0

        if (mergedAudio) {
            // Use await to ensure playback completes before moving on
            await mergedAudio.pause()
            mergedAudio.currentTime = 0
        }

        isPaused = true
    }


    onMount(async () => {
        await handleReloadBook()
        await handleReloadAudios()
    })

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
                <audio bind:this={audioList[i]} src={`${AUDIO_PATH}\\${$selected_book}\\${i}.wav`}></audio>

                <tr class="book-table-row">
                    <td class="book-table-line-number">{i}</td>
                    <td>
                        <textarea class="book-table-text" bind:value={line.line}/>
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
    <div class="generation-settings">
        <div class="book-options">
            <button class="book-options-button" on:click={() => {handleNarrateBook()}}>Narrate All</button>
            <button class="book-options-button" on:click={() => {handleMissingLines()}}>Narrate Missing</button>
            <button class="book-options-button" on:click={() => {handlePauseNarration()}}>Pause Narration</button>

            <button class="book-options-button" on:click={() => {handlePlayAll()}}>Play All</button>
            <button class="book-options-button" on:click={() => {handlePausePlaying()}}>Pause Playing</button>

            <button class="book-options-button restore" on:click={() => {handleReloadBook()}}>Undo Changes</button>
            <button class="book-options-button save" on:click={() => {handleSaveChanges()}}>Save Changes</button>

            <button class="book-options-button merge" on:click={() => {handleMergeBook()}}>Merge Book</button>
            <button class="book-options-button merge" on:click={() => {handlePlayMerged()}}>Play Merged</button>
        </div>
        <div class="voice-settings-container">
            <div class="voice-settings-row">
                <label for="voice-settings" class="voice-settings-label">Index Effect {index_effect/100}</label>
                <input type="range" bind:value={index_effect} min="0" max="100" class="voice-settings-slider" id="volume-slider">
            </div>

            <div class="voice-settings-row">
                <label for="voice-settings" class="voice-settings-label">Voice Pitch {voice_pitch}</label>
                <input type="range" bind:value={voice_pitch} min="-16" max="16" class="voice-settings-slider" id="volume-slider">
            </div>
        </div>
    </div>
</div>
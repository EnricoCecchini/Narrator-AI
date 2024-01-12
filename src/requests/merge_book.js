import { API_ROUTE } from "./api";

// Check all lines are narrated
export const check_narrated_lines = async (book) => {
    const response = await fetch(API_ROUTE + `/check_all_audios_exist`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({book})
    })

    const data = await response.json()

    return data.success
}

// Merge all generated audios into single .wav file
export const merge_book = async (book) => {
    const response = await fetch(API_ROUTE + `/merge_book`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({book})
    })

    const data = await response.json()

    return data.success
}
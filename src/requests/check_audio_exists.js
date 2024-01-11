import { API_ROUTE } from "./api";

export const check_audio_exists = async (audio_path) => {
    // Replace backslashes with forward slashes
    audio_path = audio_path.replace(/\\/g, '/')

    const audio_path_json = JSON.stringify({audio_path: audio_path})

    console.log('AUDIO PATH JSON: ', audio_path_json)

    const response = await fetch(API_ROUTE + `/check_audio_exists`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: audio_path_json
    })

    const data = await response.json()

    console.log('DATA: ', data)

    return data.success
}
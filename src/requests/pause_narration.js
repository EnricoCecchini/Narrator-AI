import { API_ROUTE } from "./api";

export const pause_narration = async () => {
    console.log('PAUSING NARRATION')

    const resp = await fetch(API_ROUTE + '/pause_narration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        return data
    })
    .catch(e => {
        console.log(e)
    })
}
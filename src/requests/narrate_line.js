import { API_ROUTE } from "./api";

export const narrate_line = async (line) => {
    console.log(line)

    const resp = await fetch(API_ROUTE + '/narrate_line', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(line)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        alert(data.message)
        return data
    })
    .catch(e => {
        console.log(e)
    })
}
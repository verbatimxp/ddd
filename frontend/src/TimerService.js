import axios from 'axios';
const API_URL = 'http://0.0.0.0:8080';


export default class TimerService{

    getTimer(data) {
        const url = `${API_URL}/${data}`;
        return axios.get(url).then(response => {
        return response.data
        })
    }
}
import axios from "axios";
import { API_URL } from "../constants";

export async function get_data() {
    const response = await axios.get(API_URL + "/test_info");
    return response.data.percentages;
}
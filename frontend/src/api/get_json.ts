import axios from "axios";
import { API_URL } from "../constants";

export async function get_json() {
   axios.get(API_URL + '/analyze-duration')
}
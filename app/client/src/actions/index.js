import { GET_BY_SEARCH, GET_BY_ID } from "../constants/actionTypes";
import * as api from "../api";

export const getProductsBySearch = (searchQuery) => async (dispatch) => {
    try {
        console.log(searchQuery);
        const { data } = await api.getProductsbySearch(searchQuery);
        dispatch({ type: GET_BY_SEARCH, payload: data });
        console.log(data);
    } catch (error) {
        console.log(error);
    }
};

export const getProductById = (id) => async (dispatch) => {
    try {
        const { data } = await api.getProductbyId(id);
        console.log(data);
        dispatch({ type: GET_BY_ID, payload: data });
    } catch (error) {
        console.log(error);
    }
};
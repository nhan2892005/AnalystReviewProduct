import { GET_BY_SEARCH, GET_BY_ID } from '../constants/actionTypes.js';

const initialState = [];

const productsReducer = (state = initialState, action) => {
    switch (action.type) {
        case GET_BY_SEARCH:
            return {
                ...state,
                search: action.payload
            };
        case GET_BY_ID:
            return {
                ...state,
                product: action.payload
            };
        default:
            return state;
    }
}

export default productsReducer;
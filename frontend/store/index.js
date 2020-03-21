import Vue from 'vue'
import { uuid } from 'uuidv4';

export const state = () => ({
    socket: {
        connected: false,
        connection_guard: false,
        failed: false,
    },
    boards: {},
    requests: {},
})

const response_handlers = {
    board_list (state, payload) {
        for (let board of payload.boards) {
            state.boards = {...state.boards, [board.pk]: board };
        }
    },

    board_detail (state, payload) {
        state.boards = {...state.boards, [payload.board.pk]: payload.board };
    },

    thread_list (state, payload) {
        console.log(payload);
        state.boards = { ...state.boards, [payload.board.pk]: payload.board };
        state.boards[payload.board.pk] = 
            {
                ...state.boards[payload.board.pk], 
                threads: state.boards[payload.board.pk]["threads"] || {}
            };
    
        for (let thread of payload.threads) {
            state.boards[payload.board.pk]["threads"] = {...state.boards[payload.board.pk]["threads"], [thread.pk]: thread };
        }
    }
}

function send_event({commit, state}, type, params) {
    const nonce = uuid();
    if (state.socket.connected && !state.socket.failed) {
        commit('set_request_status', { nonce: nonce, status: REQUEST_STATUS.PENDING });
        Vue.prototype.$socket.sendObj({ type: type, nonce: nonce, ...params });
    } else {
        commit('set_request_status', { nonce: nonce, status: REQUEST_STATUS.FAILED });
        console.warn(`Calling ${type} before connection is ready!`);
    }
    return nonce;
}

export const REQUEST_STATUS = {
    PENDING: 'pending',
    COMPLETE: 'complete',
    FAILED: 'failed',
    TIMED_OUT: 'timed_out'
}

export const actions = {
    board_list (store) {
        return send_event(store, "board_list", {});
    },
    board_detail (store, pk) {
        return send_event(store, "board_detail", {pk: pk});
    },
    thread_list (store, pk) {
        return send_event(store, "thread_list", {pk: pk});
    },
    thread_detail (store, pk) {
        return send_event(store, "thread_detail", {pk: pk});
    },
    watch_thread (store, pk) {
        return send_event(store, "watch_thread", {pk: pk});
    },
}

export const mutations = {
    SOCKET_ONOPEN (state, event) {
        //Vue.prototype.$socket = event.currentTarget
        console.log("Connected!");
        state.socket.connected = true;
        state.socket.connection_guard = true;
        //Vue.prototype.$socket.sendObj({ type: "board_list" });
    },
    SOCKET_ONCLOSE (state, event)  {
        state.socket.connected = false;
    },
    SOCKET_ONERROR (state, event)  {
        console.error(state, event);
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
        const type = message["type"];
        const nonce = message["nonce"];
        response_handlers[type](state, message);
        state.requests = { ...state.requests, [nonce]: REQUEST_STATUS.COMPLETE};
    },
    SOCKET_RECONNECT(state, count) {
        console.info(state, count);
    },
    set_request_status(state, {nonce, status}) {
        state.requests = { ...state.requests, [nonce]: status};
    },
}


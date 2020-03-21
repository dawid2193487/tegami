import Vue from 'vue'

export const state = () => ({
    socket: {
        connected: false,
        connection_guard: false,
        failed: false,
    },
    boards: {}

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
        state.boards[payload.board.pk] = {...state.boards[payload.board.pk], threads: state.boards[payload.board.pk]["threads"] || {}}
    

        for (let thread of payload.threads) {
            state.boards[payload.board.pk]["threads"] = {...state.boards[payload.board.pk]["threads"], [thread.pk]: thread };
        }
    }
}

export const actions = {
    board_detail ({commit, state}, pk) {
        if (state.socket.connected) {
            Vue.prototype.$socket.sendObj({ type: "board_detail", pk: pk });
        } else {
            console.warn("Calling board_detail before connection is ready!");
        }
    },
    thread_list ({commit, state}, pk) {
        if (state.socket.connected) {
            Vue.prototype.$socket.sendObj({ type: "thread_list", pk: pk });
        } else {
            console.warn("Calling thread_list before connection is ready!");
        }
    },
    thread_detail ({commit, state}, pk) {
        if (state.socket.connected) {
            Vue.prototype.$socket.sendObj({ type: "thread_detail", pk: pk });
        } else {
            console.warn("Calling thread_detail before connection is ready!");
        }
    },
    watch_thread ({commit, state}, pk) {
        if (state.socket.connected) {
            Vue.prototype.$socket.sendObj({ type: "watch_thread", pk: pk });
        } else {
            console.warn("Calling watch_thread before connection is ready!");
        }
    },
}

export const mutations = {
    SOCKET_ONOPEN (state, event) {
        //Vue.prototype.$socket = event.currentTarget
        console.log("Connected!");
        state.socket.connected = true;
        state.socket.connection_guard = true;
        Vue.prototype.$socket.sendObj({ type: "board_list" });
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
        response_handlers[type](state, message);
    },
    SOCKET_RECONNECT(state, count) {
        console.info(state, count);
    },
}


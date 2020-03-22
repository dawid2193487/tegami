import Vue from 'vue'
import { uuid } from 'uuidv4';

export const state = () => ({
    socket: {
        connected: false,
        connection_guard: false,
        failed: false,
    },
    boards: {},
    threads: {},
    replies: {},
    profiles: {},
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
        // state.boards = { ...state.boards, [payload.board.pk]: payload.board };

        // for (let thread of payload.threads) {
        //     state.threads = {...state.threads, [thread.pk]: {...state.threads[thread.pk], ...thread }};
        // }

        // const pks = payload.threads.map((thread) => thread.pk);

        // for (let pk of pks) {
        //     state.boards[payload.board.pk] = 
        //         {
        //             ...state.boards[payload.board.pk], 
        //             threads: { ...state.boards[payload.board.pk].threads, [pk]: pk }
        //         };
        // }
    },

    thread_detail (state, payload) {
        state.threads = {...state.threads, [payload.thread.pk]: { ...state.threads[payload.thread.pk], ...payload.thread } };
        // state.boards[payload.thread.board] = 
        //     {
        //         ...state.boards[payload.thread.board], 
        //         threads: { ...state.boards[payload.thread.board].threads, [payload.thread.pk]: payload.thread.pk }
        //     };
    },

    reply_list (state, payload) {
        //console.log(payload);
        /*for (let reply of payload.replies) {
            state.replies = {...state.replies, [reply.pk]: reply };
        }

        const pks = payload.replies.map((reply) => reply.pk);
        console.log(state.threads[payload.thread.pk]);
        state.threads[payload.thread.pk] = 
            {
                ...state.threads[payload.thread.pk], 
                replies: {}
            };
        console.log(state.threads[payload.thread.pk]);

        console.log(`Adding replies to thread ${payload.thread.pk}, pks: ${pks}`);
        for (let pk of pks) {
            state.threads[payload.thread.pk] = 
                {
                    ...state.threads[payload.thread.pk], 
                    replies: { ...state.threads[payload.thread.pk].replies, [pk]: pk }
                };
        }*/
    },

    reply_detail (state, payload) {
        state.replies = {
            ...state.replies, 
            [payload.reply.pk]: { 
                ...state.replies[payload.reply.pk], 
                ...payload.reply 
            } 
        };
        // state.threads[payload.reply.reply_to] = {
        //     ...state.threads[payload.reply.reply_to], 
        //     replies: { ...state.threads[payload.reply.reply_to].replies, [payload.reply.pk]: payload.reply.pk }
        // };
    },

    profile_detail (state, payload) {
        state.profiles = {...state.profiles, [payload.profile.pk]: payload.profile };
    },

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
    profile_detail (store, pk) {
        return send_event(store, "profile_detail", {pk: pk});
    },
    reply_list (store, pk) {
        return send_event(store, "reply_list", {pk: pk});
    },
    reply_detail (store, pk) {
        return send_event(store, "reply_detail", {pk: pk});
    }
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


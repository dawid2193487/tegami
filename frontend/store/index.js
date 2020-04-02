import Vue from 'vue'
import { uuid } from 'uuidv4';
import { rgb_to_hsl } from '~/assets/rgb_to_hsl';

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
    promises: {},
    queue: [],
    preview: "",
});

function copystamp(payload, target) {
    target["nonce"] = payload["nonce"];
    target["timestamp"] = payload["timestamp"];
}

const CACHE_DURATION = 25 * 1000;

function cached(set, pk) {
    const obj = set[pk];
    if (obj == undefined) {
        console.log("cache miss!")
        return false;
    }
    const current = Date.now();
    if (current - obj.timestamp < CACHE_DURATION) {
        console.log("cache hit!");
        return Promise.resolve();
    }
    console.log(`cache stale! ${current - obj.timestamp} old.`)
    return false;
}

const response_handlers = {
    board_list (state, payload) {
        for (let board of payload.boards) {
            let target = {};
            const prev = state.boards[board.pk];
            Object.assign(target, prev, board)
            state.boards = {...state.boards, [board.pk]: target };
        }
    },

    board_detail (state, payload) {
        copystamp(payload, payload.board);
        state.boards = {...state.boards, [payload.board.pk]: payload.board };
    },

    thread_list (state, payload) {
        // state.boards = { ...state.boards, [payload.board.pk]: payload.board };

        for (let thread of payload.threads) {
            copystamp(payload, thread);
            state.threads = {...state.threads, [thread.pk]: {...state.threads[thread.pk], ...thread }};
        }

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
        copystamp(payload, payload.thread);
        state.threads = {...state.threads, [payload.thread.pk]: { ...state.threads[payload.thread.pk], ...payload.thread } };
        // state.boards[payload.thread.board] = 
        //     {
        //         ...state.boards[payload.thread.board], 
        //         threads: { ...state.boards[payload.thread.board].threads, [payload.thread.pk]: payload.thread.pk }
        //     };
    },

    reply_list (state, payload) {
        //console.log(payload);
        for (let reply of payload.replies) {
            copystamp(payload, reply);
            state.replies = {...state.replies, [reply.pk]: reply };
        }
        /*
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
        copystamp(payload, payload.reply);
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
        copystamp(payload, payload.profile);
        state.profiles = {...state.profiles, [payload.profile.pk]: payload.profile };
    },

    post_reply_ok (state, payload) {

    },

    board_watched_ok(state, payload) {

    }

}

function send_event({commit, state}, type, params) {
    const nonce = uuid();
    if (state.socket.connected && !state.socket.failed) {
        //commit('set_request_status', { nonce: nonce, status: REQUEST_STATUS.PENDING });
        let p = new Promise((resolve, reject) => {
            commit('register_promise', {nonce, resolve, reject});
        })
        Vue.prototype.$socket.sendObj({ type: type, nonce: nonce, ...params });
        return p;
    } else {
        commit('queue', () => send_event({commit, state}, type, params));
        console.warn(`Calling ${type} before connection is ready! Queued.`);
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
        console.log(store.state.boards);
        return cached(store.state.boards, pk) || send_event(store, "board_detail", {pk: pk});
    },
    thread_list (store, pk) {
        return send_event(store, "thread_list", {pk: pk});
    },
    thread_detail (store, pk) {
        return cached(store.state.threads, pk) || send_event(store, "thread_detail", {pk: pk});
    },
    watch_thread (store, pk) {
        return send_event(store, "watch_thread", {pk: pk});
    },
    watch_board (store, pk) {
        return send_event(store, "watch_board", {pk: pk});
    },
    profile_detail (store, pk) {
        return cached(store.state.profiles, pk) || send_event(store, "profile_detail", {pk: pk});
    },
    reply_list (store, pk) {
        return send_event(store, "reply_list", {pk: pk});
    },
    reply_detail (store, pk) {
        return cached(store.state.replies, pk) || send_event(store, "reply_detail", {pk: pk});
    },
    post_reply (store, {pk, message, upload_tokens}) {
        console.log("posting!");
        console.log(`in action: ${message}`);
        return send_event(store, "post_reply", {
            pk: pk,
            message: message,
            upload_tokens
        });
    },
    post_thread(store, {pk, message, upload_tokens}) {
        return send_event(store, "post_thread", {
            pk: pk,
            message: message,
            upload_tokens
        });
    },
}

function resolve_promise(state, {nonce, value}) {
    let resolve = state.promises[nonce].resolve;
    resolve(value);
    delete state.promises[nonce];
}
function reject_promise(state, {nonce, value}) {
    let p = state.promises[nonce];
    if (p) {
        console.log(nonce);
        p.reject(value);
        delete state.promises[nonce];
        return 
    } 
    console.log("promise not found.");
}

export const mutations = {
    SOCKET_ONOPEN (state, event) {
        //Vue.prototype.$socket = event.currentTarget
        console.log("Connected!");
        state.socket.connected = true;
        state.socket.connection_guard = true;
        for (let f of state.queue) {
            f()
        }
        state.queue = [];
        //Vue.prototype.$socket.sendObj({ type: "board_list" });
    },
    SOCKET_ONCLOSE (state, event)  {
        state.socket.connected = false;
    },
    SOCKET_ONERROR (state, event)  {
        console.error(state, event);
        state.socket.failed = true;
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
        const type = message["type"];
        const nonce = message["nonce"];
        const handler = response_handlers[type];
        if (handler == undefined) {
            //state.requests = { ...state.requests, [nonce]: REQUEST_STATUS.FAILED};
            reject_promise(state, { nonce, value: `unimplemented ${type}`});
            console.log(`unimplemented ${type}`);
            console.log(message);
            return;
        }
        message["timestamp"] = Date.now();
        handler(state, message);
        //state.requests = { ...state.requests, [nonce]: REQUEST_STATUS.COMPLETE};
        resolve_promise(state, {nonce, value: "ok"});
    },
    SOCKET_RECONNECT(state, count) {
        console.info(state, count);
    },
    set_request_status(state, {nonce, status}) {
        state.requests = { ...state.requests, [nonce]: status};
    },
    register_promise(state, {nonce, resolve, reject}) {
        state.promises = { ...state.promises, [nonce]: { resolve, reject }};
    },
    resolve_promise(state, {nonce, value}) {
        let resolve = state.promises[nonce].resolve;
        resolve(value);
        delete state.promises[nonce];
    },
    reject_promise(state, {nonce, value}) {
        let p = state.promises[nonce];
        if (p) {
            console.log(nonce);
            p.reject(value);
            delete state.promises[nonce];
            return 
        } 
        console.log("promise not found.");
    },
    queue(state, f) {
        if (state.socket.connected && !state.socket.failed) {
            f();
        } else {
            state.queue = [...state.queue, f];
        }
    },
    set_preview(state, path) {
        state.preview = path;
    }
}


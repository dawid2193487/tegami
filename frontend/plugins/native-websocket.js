import Vue from 'vue'
import VueNativeSock from 'vue-native-websocket'

export default ({ store }, inject) => {
    Vue.use(VueNativeSock, 'ws://localhost:8000/ws/', { store: store, format: 'json' })
}
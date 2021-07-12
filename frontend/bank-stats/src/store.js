import { createStore } from 'vuex'


const state = {
	currTab: 'Incoming'
}

const mutations = {
	changeTab(state, payload) {
		state.currTab = payload
	}
}

const getters = {
	getCurrTab: state => state.currTab
}


export const store = createStore({
	state,
	mutations,
	getters
})
import { createStore } from 'vuex'

const state = {
	currTab: 'Incoming',
	currMonth: 1
}

const mutations = {
	changeTab(state, payload) {
		state.currTab = payload
	},
	changeMonth(state, payload) {
		state.currMonth = payload
		console.log("state month changed to ", payload)
	}
}

const getters = {
	getCurrTab: state => state.currTab,
	getCurrMonth: state => state.currMonth
}

const store = createStore({
	state,
	mutations,
	getters
})

export default store
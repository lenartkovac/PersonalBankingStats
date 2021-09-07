import { createStore } from 'vuex'

const state = {
	currTab: 'Incoming',
	date: new Date()
};

const mutations = {
	changeTab(state, payload) {
		state.currTab = payload;
	},
	UPDATE_DATE(state, payload) {
		state.date = payload;
	}
};

const actions = {
	changeDate({commit, state}, {monthDiff, yearDiff}) {
		let newDate = new Date(state.date);
		newDate.setMonth(newDate.getMonth() + monthDiff);
		newDate.setYear(newDate.getFullYear() + yearDiff);

		// new Date cannot be in the future
		newDate = new Date(Math.min(newDate, new Date()));
		commit('UPDATE_DATE', newDate);
	}
};

const getters = {
	currTab: state => state.currTab,
	currDate: state => state.date
};

const store = createStore({
	state,
	actions,
	mutations,
	getters
});

export default store
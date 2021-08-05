<template>
	<div class='tabs'>
    <!-- Tab list --> 
		<ul class='tabs__header'>
			<li v-for='tab in tabs'
				:key="tab.props.title"
				@click='selectTab(tab.props.title)'
				:class='{"tab__selected": (tab.props.title == selectedTab)}'
				>
				{{tab.props.title}}
			</li>
		</ul>
    <!-- slots --> 
    <slot></slot>
	</div>
</template>

<script>
import {
  onMounted,
  provide,
  reactive,
  toRefs
} from "vue"

import { useStore } from 'vuex'

export default {
	setup(_, {slots}) {
    const state = reactive ({
      selectedTab: null,
      tabs: slots.default()
    });

    provide("TabsProvider", state);

    const selectTab = (i) => {
      state.selectedTab = i;
      store.commit('changeTab', i)
    }

    const store = useStore()

    //onMounted(() => state.selectedTab = store.state.currTab)
    onMounted(() => state.selectedTab = store.getters.getCurrTab)

    return { ...toRefs(state), selectTab}
  },
}
</script>

<style scoped>
  ul.tabs__header {
    display: block;
    list-style: none;
    margin: 0 0 0 20px;
    padding: 0;
  }
  ul.tabs__header > li {
    padding: 15px 30px;
    border-radius: 10px;
    margin: 0;
    display: inline-block;
    margin-right: 5px;
    cursor: pointer;
  }
  ul.tabs__header > li.tab__selected {
    font-weight: bold;
    border-radius: 10px 10px 0 0;
    border-bottom: 8px solid transparent;
  }
  .tab {
    display: inline-block;
    color: black;
    padding: 20px;
    min-width: 800px;
    border-radius: 10px;
    min-height: 400px;
  }
  .tabs .tab{
    background-color: #fff;
  }
  .tabs li {
    background-color: #ddd;
    color: #aaa;
  }
  .tabs li.tab__selected {
    background-color: #fff;
    color: #83FFB3;
  }
</style>
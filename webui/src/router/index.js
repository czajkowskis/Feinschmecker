import { createRouter, createWebHistory } from 'vue-router';
import HomeView from "../views/HomeView.vue"
import RecipeView from "../views/RecipeView.vue"
const router = createRouter({
  history: createWebHistory(),
	routes: [
		{path: '/', name: 'Home', component: HomeView},
		{path: '/recipe', name: 'Recipe', component: RecipeView},
	],
	scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, behavior: 'auto' };
    }
    return { top: 0 };
  },
});

export default router;

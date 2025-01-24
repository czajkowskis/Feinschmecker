<script>
  import Navbar from "./components/Navbar.vue"
  import HeroHeader from "./components/HeroHeader.vue"
  import AboutUs from "./components/AboutUs.vue"
  import SearchSection from "./components/SearchSection.vue"
  import RecipesSection from "./components/RecipesSection.vue"
  export default {
    components: {
      Navbar,
      HeroHeader,
      AboutUs,
      SearchSection,
      RecipesSection
    },

    data() {
      return {
        recipes: []
      }
    },

    methods: {
      handleSearchAction(recipes){
        this.recipes = recipes 
        console.log(this.recipes)
      }
    }
  }
</script>

<template>
  <Navbar v-motion-slide-left />
  <HeroHeader v-motion-slide-right/>
  <AboutUs/>
  <SearchSection @searched="handleSearchAction"/>
  <RecipesSection :recipes="this.recipes"/>
</template>
<style scoped>
  body {
    background: #F0F8FF;
  }
  

</style>


<script>
  import Navbar from "../components/Navbar.vue"
  import HeroHeader from "../components/HeroHeader.vue"
  import AboutUs from "../components/AboutUs.vue"
  import SearchSection from "../components/SearchSection.vue"
  import RecipesSection from "../components/RecipesSection.vue"
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
        recipes: [],
        maxRecipesShown: 0,
      }
    },

    methods: {
      handleSearchAction(recipes){
        this.recipes = recipes;
        this.maxRecipesShown = 6;
        console.log(this.recipes)
      },

      scrollToAboutUs(){
        this.$refs.aboutUs.$el.scrollIntoView({behavior: "smooth"})
      },

      scrollToSearchSection(){
        this.$refs.searchSection.$el.scrollIntoView({behavior: "smooth"})
      },

      handleLoadMoreRecipes(){
        if(this.maxRecipesShown < this.recipes.length) {
          this.maxRecipesShown += 6
        }
        console.log(this.maxRecipesShown)
      }
    }
  }
</script>

<template>
  <Navbar @scrollToAboutUs="scrollToAboutUs" @scrollToSearchSection="scrollToSearchSection" v-motion-slide-left />
  <HeroHeader @scrollToAboutUs="scrollToAboutUs" @scrollToSearchSection="scrollToSearchSection" v-motion-slide-right/>
  <AboutUs ref="aboutUs"/>
  <SearchSection id="search-section" ref="searchSection" @searched="handleSearchAction"/>
  <RecipesSection @loadMoreRecipes="handleLoadMoreRecipes" :recipes="this.recipes" :maxRecipesShown="maxRecipesShown"/>
</template>
<style scoped>
  body {
    background: #F0F8FF;
  }
  

</style>


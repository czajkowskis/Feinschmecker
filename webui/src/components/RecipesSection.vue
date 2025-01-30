<script>
  import RecipeCard from "./RecipeCard.vue"

  export default {
    components: {
      RecipeCard
    },
    props: {
      recipes: {
        required: true
      },
      maxRecipesShown:{
        type: Number,
        required: true,
      }
    },
    methods: {
      loadMoreRecipes(){
        this.$emit("loadMoreRecipes")
        console.log("load")
      },
    }
  }

</script>

<template>
  <section class="recipe-section">
    <h1 v-if="this.recipes.length>0" v-motion-slide-right>We found {{this.recipes.length}} recipes for you!</h1>
    <div class="container">
      <RecipeCard v-motion-slide-right v-for="recipe in recipes.slice(0, maxRecipesShown)" :key="recipe.name" :recipe="recipe" photo_src="/images/recipe_images/breakfast_burrito.png"/>
      <button v-if="maxRecipesShown < this.recipes.length" @click="loadMoreRecipes">Show more recipes</button>
    </div>
  </section>
</template>

<style scoped>
  
  .recipe-section {
    background: #F0F8FF;
    margin: 0 auto;
    width: 100%;
  }
  
  .container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
    width: 70%;
    margin: 50px auto;
  }

  .top-container {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 20px 0;
  }


  .bottom-container {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 20px 0;
  }

  img {
    width: 40%;
  }

  .top-container > img {
    width: 50%;
    margin-right: 80px;
  }

  .bottom-container > img {
    margin-left: 100px;
  }

  h1 {
    font-family: "Poppins";
    font-size: 48px;
    font-weight: 700;
    margin: 30px 0;
  }

  p {
    font-family: "Poppins";
    font-size: 28px;
    font-weight: 400;
    text-align: justify;
  }


  button {
    background: #F0F8FF;
    font-family: "Poppins";
    font-size: 28px;
    font-weight: 700;
    border: 2px solid #000;
    border-radius: 30px;
    padding: 10px 50px;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
  }

  button:hover {
    background-color: #DCEEFF
  }
</style>

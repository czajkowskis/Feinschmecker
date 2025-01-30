<script>
  import MacronutrientsSummary from "../components/MacronutrientsSummary.vue"
  import { nextTick } from "vue";
  export default {
    components: {
      MacronutrientsSummary
    },
    data() {
      return {
        recipe: JSON.parse(localStorage.getItem('current_recipe')) || [],
      }
    },

    methods: {
      handleSearchAction(recipes){
        this.recipes = recipes 
        console.log(this.recipes)
      },
      goBack(){
        this.$router.push({name: "Home", hash:'#search-section'});
      },
    },
    mounted() {
      window.scrollTo(0, 0);
    }
  }
</script>

<template>
  <div class="container">
    <div class="left-container">
      <div class="button-container">
        <button @click="goBack">Back</button>
      </div>
      <div class="recipe-info-box">
        <img :src="recipe.image_link"/>
        <MacronutrientsSummary :calories="recipe.calories" :protein="recipe.protein" :carbohydrates="recipe.carbohydrates" :fat="recipe.fat"/>
        <p><strong>Authored by:</strong> {{recipe.author}}</p>
        <p><strong>Scraped from:</strong> <a :href="recipe.source_link">{{recipe.source_name}}</a></p>
      </div>
    </div>
    <div class ="right-container">
      <h1>{{recipe.name}}</h1>

      <div class="ingredients-box">
        <h2>Ingredients</h2>
        <div class="ingredients-names-box">
          <p v-for="(ingredient, index) in recipe.ingredients.split('#')" :key="index">{{ingredient}}</p>
        </div>
      </div>
      <div class="instructions-box">
        <h2>Instructions</h2>
        <div class="instructions-paragraphs-box">
          <p v-for="(step, index) in recipe.instructions" :key="index"><span class="instruction-index">{{index+1}}</span> {{step}}</p>
        </div> 
      </div>
    </div>
  </div>
</template>
<style scoped>
  body {
    background: #F0F8FF;
  }

  .container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    height:90vh;
  }

  .left-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 30%;
    height: 100%;
  }

  .button-container {
    display: flex;
    justify-content: flex-start;
    width: 90%;
  }

  .recipe-info-box {
    padding: 50px;
  }

  .right-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: 60%;
    height: 100%;
  }

  .ingredients-box {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    border: 3px solid #000;
    border-radius: 30px;
    padding: 30px 20px;
    background-color: #FFEE8C;
  }

  .ingredients-names-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
  }

  .instructions-box {
    margin: 50px 0;
    padding: 30px 20px;
    border: 3px solid #000;
    border-radius: 30px;
  }

  h1 {
    font-family: "Poppins";
    font-size: 64px;
  }

  h2 {
    font-family: "Poppins";
    font-size: 32px;
    margin: 0;
    padding: 0;
  }

  p {
    font-family: "Poppins";
    font-size: 18px;
    text-align: justify;
  }

  .instruction-index {
    font-size: 22px;
    font-weight: 700;
  }

  button {
    padding: 10px 20px;
    margin: 50px 20px;
    font-family: "Poppins";
    font-size: 24px;
    border: 2px solid #000000;
    border-radius: 10px;
    cursor: pointer;
    background-color: #F0F8FF;
    transition: 0.3s all ease-in-out;
  }

  button:hover {
    background-color: #DCEEFF
  }

  img {
    max-width: 400px;
  }
</style>

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
    },
  }
</script>

<template>
  <section class="recipe-section">
    <div class="container">
      <RecipeCard v-motion-slide-right v-for="recipe in recipes" :key="recipe.name" :recipe_title="recipe.name" photo_src="/images/recipe_images/breakfast_burrito.png"/>
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
    padding: 10px 20px;
    font-family: "Poppins";
    font-size: 28px;
    border: 2px solid #000000;
    border-radius: 10px;
  }

  .secondary-button {
    background: #F0F8FF;
  }

  .primary-button {
    background-color: #FFEE8C;
  }
</style>

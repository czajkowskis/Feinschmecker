<script>

  export default {
    props: {
      recipe: {
        required: true
      },
    },
    methods: {
      goToRecipe(){
        localStorage.setItem('current_recipe', JSON.stringify(this.recipe));
        this.$router.push({ name: 'Recipe'});
      }
    }
  }
</script>


<template>
  <div class="card">
    <img :src="recipe.image_link"/>
    <h1> {{this.recipe.name}}</h1>
    <button @click="goToRecipe">Details</button>
  </div>
</template>


<style scoped>
  
  .card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 25%;
    min-height: 60vh;
    border: 3px solid #000;
    padding: 0 20px;
    margin: 30px;
  }

  img {
    width: 300px;
    border-radius: 50px;
    margin: 30px 0 10px 0;
  }

  h1 {
    font-family: "Poppins";
    font-size: 28px;
    font-weight: 700;
    margin-top: 20px;
  }

  button {
    padding: 10px 50px;
    font-family: "Poppins";
    font-size: 28px;
    border: 2px solid #000000;
    border-radius: 10px;
    cursor: pointer;
    background-color: #FFEE8C;
    margin-bottom: 20px;
    transition: all 0.3s ease-in-out;
  }
  
  button:hover {
    background-color: #ffde4d;
  }

</style>

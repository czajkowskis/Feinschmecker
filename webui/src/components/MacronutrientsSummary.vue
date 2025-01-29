<script>
  export default {
    props: {

      calories: {
        type: Number,
        required: true,
      },

      protein: {
        type: Number,
        required: true,
      },

      carbohydrates: {
        type: Number,
        required: true,
      },

      fat: {
        type: Number,
        required: true,
      },
    }
  }
</script>

<template>
  <div class="summary-container">
    <div class="nutrient-container">
      <h1>{{this.calories}}</h1>
      <h2>Calories</h2>
    </div>
    <div class="nutrient-container">
      <h1>{{this.protein}}</h1>
      <h2>Protein</h2>
    </div>
    <div class="nutrient-container">
      <h1>{{this.carbohydrates}}</h1>
      <h2>Carbs</h2>
    </div>
    <div class="nutrient-container">
      <h1>{{this.fat}}</h1>
      <h2>Fats</h2>
    </div>
  </div>
</template>

<style scoped>
  
  .summary-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 70%;
    margin: 10px 0;
  }

  .nutrient-container {
    display: flex;
    flex-direction: column;
    padding: 20px;
  }

  h1 {
    font-family: "Poppins";
    font-size: 28px;
    font-weight: 700;
    margin: 0;
  }

  h2 {
    font-family: "Poppins";
    font-size: 18px;
    font-weight: 400;
    margin-top: 10px;
  }
  
</style>

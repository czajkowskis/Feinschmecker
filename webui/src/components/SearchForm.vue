<script>
  export default {
    data() {
      return {
        calories: "",
        protein: "",
        carbs: "",
        fats: "",
        time: "",
        difficulty: 0,
        vegetarian: false,
        vegan: false,
        mealtype: "",
        recipes: [],
      }
    },
    methods: {
      getQueryParametersDictionary() {
        const queryParameters = {
          calories_smaller: this.calories,
          protein_bigger: this.protein,
          fats_bigger: this.fats,
          carbohydrates_bigger: this.carbs,
          vegetarian: this.vegetarian,
          vegan: this.vegan,
        }
        
        if(this.time.length > 0) {
          queryParameters["time"] = this.time
        }

        if(this.difficulty != 0) {
          queryParameters["difficulty"] = this.difficulty
        }

        if(this.mealtype.length > 0) {
          queryParameters["meal_type"] = this.mealtype
        }

        return queryParameters
      },

      async getRecipes(){
        const queryParameters = this.getQueryParametersDictionary()
        console.log(queryParameters)
        try {
            let response = await this.$axios.get("/recipes", {
              params: queryParameters, 
            })
            this.recipes = response.data
            this.$emit("searched", this.recipes)
            console.log(this.recipes);
        } catch(err) {
            console.log(err.response.data);
        }
      },
    },
  }
</script>

<template>
  <div class="form-container">
    <div class="top-container">
      <div class="macronutrients-container">
        <div class="title-container">
          <h1>Macronutrients</h1>
          <span>(amount in grams)</span> 
        </div>
        <div class="input-container">
          <div class="input-label-pair">
            <input v-model="calories" id="calories" class="rectangular-input"/>
            <label for="calories">Calories</label>
          </div>
          <div class="input-label-pair">
            <input v-model="protein" id="protein" class="rectangular-input"/>
            <label for="protein">Protein</label>
          </div>
          <div class="input-label-pair">
            <input v-model="carbs" id="carbs" class="rectangular-input"/>
            <label for="carbs">Carbs</label>
          </div>
          <div class="input-label-pair">
            <input v-model="fats" id="fats" class="rectangular-input"/>
            <label for="fats">Fats</label>
          </div>
        </div>
      </div>
    </div>
    <div class="middle-container">
      <div class="middle-left-container">
        <div class="title-container">
          <h1>Preparation time</h1>
          <span>(in minutes)</span>
        </div>
        <input v-model="time" class="rectangular-input"/>
      </div>
      <div class="middle-right-container">
        <div class="difficulty-container">
          <h1>Difficulty</h1>
          <div class="difficulty-input-container">
            <div class="input-label-pair">
              <input v-model="difficulty" name="difficulty" id="easy" value="1" type="radio">
              <label for="easy">Easy</label>
            </div>
            <div class="input-label-pair">
              <input v-model="difficulty" name="difficulty" id="medium" value="2" type="radio">
              <label for="medium">Medium</label>
            </div>
            <div class="input-label-pair">
              <input v-model="difficulty" name="difficulty" id="hard" value="3" type="radio">
              <label for="hard">Hard</label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="bottom-container">
      <div>
        <input v-model="vegetarian" id="vegetarian-input" type="checkbox">
        <label for="vegetarian-input">Vegetarian</label>
      </div>
      <div>
        <input v-model="vegan" id="vegan-input" type="checkbox">
        <label for="vegan-input">Vegan</label>
      </div>
      <select v-model="mealtype" name="mealtype" id="mealtype-select">
        <option disabled value="">Select the mealtype</option>
        <option value="breakfast">Breakfast</option>
        <option value="dinner">Dinner</option>
        <option value="dessert">Dessert</option>
      </select>
    </div>
    <div class="button-container">
      <button @click="getRecipes">Search</button>
    </div>
  </div>
</template>

<style scoped>
  
  .form-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    width: 50%;
    margin: 20px auto;
  }

  .top-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 0;
  }

  .macronutrients-container {
    width: 100%;
    padding: 0 100px 50px 100px;
    border: 4px solid #000;
    border-radius: 30px;
  }


  .title-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
  }

  span {
    font-family: "Poppins";
    font-size: 18px;
    font-weight: 400;
  }
  
  .macronutrients-container > .input-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .input-label-pair {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .middle-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: 0 auto;
    padding: 50px 0;
  }

  .difficulty-container {
    display: flex;
    flex-direction: column;
    padding: 20px;
    border: 4px solid #000;
    border-radius: 30px;
    background-color: #FFEE8C;
  }

  .difficulty-input-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  
  .difficulty-input-container > .input-label-pair {
    margin: 20px;
  }

  .bottom-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 50px 0;
  }

  h1 {
    font-family: "Poppins";
    font-size: 32px;
    font-weight: 700;
    margin: 0;
  }

  .rectangular-input {
    width: 50px;
    height: 50px;
    padding: 10px;
    background-color: #F0F8FF;
    border: 3px solid #000;
    border-radius: 20px;
    text-align: center;
    font-family: "Poppins";
    font-size: 24px;
    font-weight: 700;
  }

  input[type=radio] {
    width: 20px;
    height: 20px;
    margin: 10px;
  }

  label {
    font-family: "Poppins";
    font-size: 24px;
  }
  
  .bottom-container > div > input[type=checkbox] {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin: 10px;
  }

  select {
    background-color: #F0F8FF;
    font-family: "Poppins";
    font-size: 18px;
    font-weight: 400;
    border: 2px solid #000;
    border-radius: 30px;
    padding: 10px 30px;
    text-align: center;
  }

  .button-container {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  button {
    background-color: #FFEE8C;
    font-family: "Poppins";
    font-size: 24px;
    font-weight: 700;
    border: 2px solid #000;
    border-radius: 30px;
    padding: 10px 50px;
    cursor: pointer;
  }
</style>

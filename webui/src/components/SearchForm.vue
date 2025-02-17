<script>
  export default {
    data() {
      return {
        calories: "",
        calories_bigger: false,
        protein: "",
        protein_bigger: true,
        carbohydrates: "",
        carbohydrates_bigger: true,
        fat: "",
        fat_bigger: true,
        time: "",
        difficulty: 0,
        vegetarian: false,
        vegan: false,
        mealtype: "",
        recipes: [],
        errorMessage: "",
        showErrorMessage: false,
        ingredients: "",
        knownIngredients: ["onion", "tomato", "garlic", "ginger", "potato",
          "carrot", "cucumber", "pepper", "chili", "lettuce",
          "spinach", "broccoli", "cabbage", "mushroom", "corn",
          "peas", "beans", "avocado", "zucchini", "eggplant", "cheese", "sugar", "salt"]
      }
    },
    methods: {
      getQueryParametersDictionary() {
        const queryParameters = {};

        if(this.calories.length != 0) {
          if(this.calories_bigger){
            queryParameters["calories_bigger"] = this.calories;
          }
          else{
            queryParameters["calories_smaller"] = this.calories;
          }
        }

        if(this.protein.length != 0) {
          if(this.protein_bigger){
            queryParameters["protein_bigger"] = this.protein;
          }
          else{
            queryParameters["protein_smaller"] = this.protein;
          }
        }

        if(this.fat.length != 0) {
          if(this.fat_bigger){
            queryParameters["fat_bigger"] = this.fat;
          }
          else{
            queryParameters["fat_smaller"] = this.fat;
          }
        }

        if(this.carbohydrates.length != 0) {
          if(this.carbohydrates_bigger){
            queryParameters["carbohydrates_bigger"] = this.carbohydrates;
          }
          else{
            queryParameters["carbohydrates_smaller"] = this.carbohydrates;
          }
        }

        if(this.vegetarian) {
          queryParameters["vegetarian"] = true;
        }

        if(this.vegan) {
          queryParameters["vegan"] = true;
        }

        if(this.time.length != 0) {
          queryParameters["time"] = this.time
        }

        if(this.difficulty != 0) {
          queryParameters["difficulty"] = this.difficulty
        }

        if(this.mealtype.length != 0) {
          queryParameters["meal_type"] = this.mealtype
        }

        if (this.ingredients !== "") {
          const ingredientsArray = this.ingredients.split(",");
          queryParameters["ingredients"] = JSON.stringify(ingredientsArray); // Serialize to JSON string
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

      parseCustomInput(input) {
        return this.knownIngredients.filter(ingredient => input.includes(ingredient));
      }
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
            <div class="switch-box">
              <span class="switch-text">&lt;</span>
              <label class="switch">
                <input v-model="calories_bigger" type="checkbox">
                <span class="slider"></span>
              </label>
              <span class="switch-text">&gt;</span>
            </div>
          </div>
          <div class="input-label-pair">
            <input v-model="protein" id="protein" class="rectangular-input"/>
            <label for="protein">Protein</label>
            <div class="switch-box">
              <span class="switch-text">&lt;</span>
              <label class="switch">
                <input v-model="protein_bigger" type="checkbox">
                <span class="slider"></span>
              </label>
              <span class="switch-text">&gt;</span>
            </div>
          </div>
          <div class="input-label-pair">
            <input v-model="carbohydrates" id="carbs" class="rectangular-input"/>
            <label for="carbs">Carbs</label>
            <div class="switch-box">
              <span class="switch-text">&lt;</span>
              <label class="switch">
                <input v-model="carbohydrates_bigger" type="checkbox">
                <span class="slider"></span>
              </label>
              <span class="switch-text">&gt;</span>
            </div>
          </div>
          <div class="input-label-pair">
            <input v-model="fat" id="fat" class="rectangular-input"/>
            <label for="fat">Fats</label>
            <div class="switch-box">
              <span class="switch-text">&lt;</span>
              <label class="switch">
                <input v-model="fat_bigger" type="checkbox">
                <span class="slider"></span>
              </label>
              <span class="switch-text">&gt;</span>
            </div>
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
        <option value="">All mealtypes</option>
        <option value="Breakfast">Breakfast</option>
        <option value="Lunch">Lunch</option>
        <option value="Dinner">Dinner</option>
      </select>
    </div>
    <div class="ingredient-container">
      <h1>Ingredients</h1>
      <input type="text" v-model="ingredients" class="ingredient-input" id="ingredients-input" placeholder="chicken,garlic,onion"/>
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

  .ingredient-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 50px 10px;
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
    max-width: 60px;
    height: 60px;
    padding: 10px;
    background-color: #F0F8FF;
    border: 3px solid #000;
    border-radius: 20px;
    text-align: center;
    font-family: "Poppins";
    font-size: 24px;
    font-weight: 700;
  }

  .ingredient-input{
    max-width: 400px;
    height: 60px;
    padding: 5px;
    margin-top: 20px;
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

  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }

  .switch input { 
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 30px;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    border-radius: 50%;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
  }

  .switch-box {
    margin-top: 10px;
  }

  .switch-text {
    font-family: "Poppins";
    font-size: 28px;
    margin: 0 5px; 
  }

</style>

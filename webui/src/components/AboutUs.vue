<script setup>
</script>

<template>
  <section class="hero-section">
    <div class="container">
      <h1>About us</h1>
      <div class="top-container">
        <img src="/images/lifestyle_icon.svg"/>
        <p>
          At <strong>Feinschmecker</strong>, we believe that cooking
          your own meals should be <strong>accessible, enjoyable, 
          and tailored to fit your unique lifestyle goals</strong>. 
          Our platform is designed to support everyone from 
          seasoned chefs to kitchen beginners in creating <strong>delicious,
          nutritious</strong> meals that align with their personal dietary needs.
        </p>
      </div>
      <div class="bottom-container">
        <p>
          Whether you're focusing on <strong>weight loss, muscle gain</strong>, or simply 
          want to <strong>eat healthier</strong>, Feinschmecker offers a suite of tools to help 
          you <strong>discover recipes</strong> with just the right nutritional balance. You can
          easily <strong>search and filter recipes</strong> based on specific dietary requirements 
          such as calorie limits, macronutrient ratios, or ingredient preferences 
          so that <strong>every meal works toward your health and fitness goals.</strong>
        </p>
        <img class="muscles_icon" src="/images/muscles_icon.svg"/>
        <img class="diet_icon" src="/images/diet_icon.svg"/>
      </div>
    </div>
  </section>
</template>

<style scoped>
  
  .hero-section {
    background: #FFEE8C;
    width: 100%;
    margin:0;
  }
  
  .container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    width: 90%;
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

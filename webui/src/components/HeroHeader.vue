<script setup>
</script>

<template>
  <header class="container">
    <div class="left-container">
      <h1>Foodies, welcome home!</h1>
      <p> Feinschmecker is the perfect companion in your cooking journey! Find new recepies, perfect meals for your nutritional goals and more! </p>
      <div class="buttons-container">
        <button @click="this.$emit('scrollToAboutUs')" class="secondary-button">About us</button>
        <button @click="this.$emit('scrollToSearchSection')" class="primary-button">Start Cooking!</button>
      </div>
    </div>
    <div class="right-container">
      <img src="/images/hero.png"/>
    </div>
  </header>
</template>

<style scoped>
  
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 90%;
    margin: 50px auto;
  }

  .left-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 40%;
  }

 .buttons-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
  }

  .right-container {
    width: 30%;
  }

  
  h1 {
    font-family: "Poppins";
    font-size: 40px;
    font-weight: 700;
    margin: 0;
  }

  p {
    font-family: "Poppins";
    font-size: 28px;
    font-weight: 400;
    text-align: justify;
    margin: 30px 0;
  }

  button {
    padding: 10px 20px;
    font-family: "Poppins";
    font-size: 28px;
    border: 2px solid #000000;
    border-radius: 10px;
    cursor: pointer;
  }

  .secondary-button {
    background-color: #F0F8FF;
    transition: 0.3s all ease-in-out;
  }

  .secondary-button:hover {
    background-color: #DCEEFF
  }

  .primary-button {
    background-color: #FFEE8C;
    transition: 0.3s all ease-in-out;
  }

  .primary-button:hover {
    background-color: #ffde4d;
  }

  img {
    margin: 0;
  }

</style>

<script setup>
</script>

<template>
  <div class="container">
    <div class="title-container">
      <img src="/images/noodles_icon.png"/>
      <h1>Feinschmecker</h1>
    </div>
    <div class="button-container">
      <button class="secondary-button">Home</button>
      <button class="secondary-button">About us</button>
      <button class="primary-button">Search</button>
    </div>
  </div> 
</template>

<style scoped>
  
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 90%;
    margin: 0 auto;
  }
  
  .title-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }

  img {
    width: 100%;
    height: 100%;
    margin-right: 40px;
  }

  .button-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  h1 {
    color: #000000;
    font-family: "Poppins";
    font-size: 48px;
    font-weight: 700;
  }

  button {
    padding: 10px 20px;
    margin: 0px 20px;
    font-family: "Poppins";
    font-size: 24px;
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
</style>

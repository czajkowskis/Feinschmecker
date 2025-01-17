<script setup>
  import SearchForm from "./SearchForm.vue"
</script>

<template>
  <section class="search-section">
    <div class="container">
      <h1 v-motion-slide-visible-once-left>Start your search</h1>
      <div class="top-container" v-motion-slide-visible-once-left>
        <p>
          Here you can enter your requirements and our system will 
          return to you with tasty recipes tailored to your needs! If 
          some aspect is not important for you leave the input blank. 
        </p>
      </div>
      <SearchForm v-motion-slide-visible-once-right/>
    </div>
  </section>
</template>

<style scoped>
  
  .hero-section {
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

</style>

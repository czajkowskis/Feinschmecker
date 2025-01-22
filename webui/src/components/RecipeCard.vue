<script>

  export default {
    props: {
      recipe_title: {
        type: String,
        required: true
      },

      photo_src: {
        type: String,
        required: true
      }
    }
  }
</script>


<template>
  <div class="card">
    <img :src="this.photo_src"/>
    <h1> {{this.recipe_title}}</h1>
    <button>Details</button>
  </div>
</template>


<style scoped>
  
  .card {
    display: flex;
    flex-direction: column;
    justify-items: space-between;
    align-items: center;
    max-width: 20%;
    border: 3px solid #000;
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
  }


</style>

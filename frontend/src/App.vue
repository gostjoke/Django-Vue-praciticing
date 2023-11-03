<!--   frontend/src/App.vue   -->

<template>

  <BlogHeader/>

  <ArticleList/>

  <BlogFooter/>

</template>

<script>
  import BlogHeader from './components/BlogHeader.vue'
  import BlogFooter from './components/BlogFooter.vue'
  import ArticleList from './components/ArticleList.vue'

  export default {
    name: 'App',
    components: { BlogHeader, BlogFooter, ArticleList}
  }

</script>

<style>
  #app{
    font-family:Georgia, 'Times New Roman', Times, serif;
    margin-left: 40px;
    margin-right: 40px;
  }
</style>

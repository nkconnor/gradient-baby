<template>
  <!-- Don't drop "q-app" class -->

  <div id="q-app">
      <div id="clouds">
	<div class="cloud x1"></div>
	<!-- Time for multiple clouds to dance around -->
	<div class="cloud x2"></div>
	<div class="cloud x3"></div>
	<div class="cloud x4"></div>
	<div class="cloud x5"></div>
</div>
    <router-view></router-view>
  </div>
</template>

<script>
/*
 * Root component
 */
export default {}
</script>

<style></style>

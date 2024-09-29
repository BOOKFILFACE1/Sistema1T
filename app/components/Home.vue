<template>
  <Page>
    <ActionBar title="FazhTech" />
    <ScrollView>
      <StackLayout class="home-panel">
        <Label text="FazhTech" class="title" />
        <Label text="Bienvenido a nuestra aplicación" class="subtitle" />
        <Button text="Entrar" @tap="onEnterTap" class="btn btn-primary" />
      </StackLayout>
    </ScrollView>
  </Page>
</template>

<script>
export default {
  methods: {
    onEnterTap() {
      this.$navigateTo(Login);
    }
  }
};
import Login from './Login';
</script>

<style scoped>
.home-panel {
  vertical-align: center;
  font-size: 20;
  margin: 15;
}

.title {
  font-size: 60;
  font-weight: bold;
  color: #4a90e2;
  text-align: center;
  margin-bottom: 20;
}

.subtitle {
  font-size: 20;
  color: #333;
  text-align: center;
  margin-bottom: 30;
}

.btn {
  font-size: 18;
  width: 200;
  background-color: #4a90e2;
  color: white;
}
</style>

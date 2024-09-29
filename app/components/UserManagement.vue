<template>
  <StackLayout>
    <Label text="Gestión de Usuarios" class="title"/>
    <TextField v-model="newUser" hint="Nombre de usuario" />
    <Button text="Agregar Usuario" @tap="addUser" class="btn btn-primary"/>
    <ListView for="user in users" class="list-group">
      <v-template>
        <Label :text="user" class="list-group-item"/>
      </v-template>
    </ListView>
  </StackLayout>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      newUser: ""
    };
  },
  methods: {
    addUser() {
      if (this.newUser.trim()) {
        this.users.push(this.newUser.trim());
        this.newUser = "";
      }
    }
  }
};
</script>

<style scoped>
.title {
  font-size: 24;
  font-weight: bold;
  margin: 10;
}
.list-group-item {
  padding: 10;
}
</style>

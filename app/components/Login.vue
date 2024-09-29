<template>
    <Page>
      <ActionBar title="FazhTech Login" />
      <ScrollView>
        <StackLayout class="login-panel">
          <Image src="~/components/h.png" class="logo" />
          <TextField v-model="username" hint="Usuario" class="input" />
          <TextField v-model="password" hint="Contraseña" secure="true" class="input" />
          <Button text="Iniciar Sesión" @tap="onLoginTap" class="btn btn-primary" />
          <Label v-if="error" :text="error" class="error-message" />
        </StackLayout>
      </ScrollView>
    </Page>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        error: ''
      };
    },
    methods: {
      onLoginTap() {
        if (this.username === 'demo' && this.password === 'demo') {
          alert('Inicio de sesión exitoso');
          // Aquí puedes navegar a la siguiente pantalla después del login
        } else {
          this.error = 'Usuario o contraseña incorrectos';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-panel {
    vertical-align: center;
    font-size: 20;
    margin: 15;
  }
  
  .logo {
    width: 150;
    height: 150;
    margin-bottom: 20;
  }
  
  .input {
    margin-bottom: 20;
    padding: 10;
    background-color: #f0f0f0;
    border-radius: 5;
  }
  
  .btn {
    font-size: 18;
    width: 200;
    background-color: #4a90e2;
    color: white;
    margin-top: 20;
  }
  
  .error-message {
    color: red;
    text-align: center;
    margin-top: 20;
  }
  </style>


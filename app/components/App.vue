<template>
  <Page>
    <ActionBar title="Mi App NativeScript" />
    <TabView>
      <TabViewItem title="Inicio">
        <ScrollView>
          <StackLayout class="home-panel">
            <Label text="Hola" class="greeting" />
            <Label text="Mundo" class="world" />
            <Label text="Bienvenido a Mi App" class="welcome" />
            <Label text="Una App Profesional en NativeScript-Vue" class="subtitle" />
            <Button text="Procesar Datos" @tap="processData" class="btn btn-primary" />
            <Label :text="processingStatus" class="status" />
          </StackLayout>
        </ScrollView>
      </TabViewItem>
      <TabViewItem title="Usuarios">
        <UserManagement />
      </TabViewItem>
      <TabViewItem title="Productos">
        <ProductManagement />
      </TabViewItem>
    </TabView>
  </Page>
</template>

<script>
import UserManagement from './components/UserManagement';
import ProductManagement from './components/ProductManagement';

export default {
  components: {
    UserManagement,
    ProductManagement
  },
  data() {
    return {
      processingStatus: ""
    };
  },
  methods: {
    processData() {
      this.processingStatus = "Procesando...";
      
      // Simulando un proceso pesado usando setTimeout
      setTimeout(() => {
        let result = 0;
        for (let i = 0; i < 1000000000; i++) {
          result += i;
        }
        
        this.processingStatus = "Proceso completado. Resultado: " + result;
      }, 0);
    }
  }
};
</script>

<style scoped>
.home-panel {
  vertical-align: center;
  font-size: 20;
  margin: 15;
}

.greeting {
  font-size: 60;
  font-weight: bold;
  color: #42b883;
  text-align: center;
}

.world {
  font-size: 50;
  font-weight: bold;
  color: #35495e;
  text-align: center;
  margin-bottom: 20;
}

.welcome {
  font-size: 30;
  font-weight: bold;
  color: #35495e;
  text-align: center;
  margin-bottom: 10;
}

.subtitle {
  font-size: 20;
  color: #666;
  text-align: center;
  margin-bottom: 30;
}

.btn {
  font-size: 18;
  width: 200;
  margin-top: 20;
}

.status {
  margin-top: 20;
  text-align: center;
  color: #42b883;
}
</style>

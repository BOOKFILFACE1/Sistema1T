<template>
  <StackLayout>
    <Label text="Gestión de Productos" class="title"/>
    <TextField v-model="newProduct.name" hint="Nombre del producto" />
    <TextField v-model="newProduct.price" hint="Precio" keyboardType="number" />
    <Button text="Agregar Producto" @tap="addProduct" class="btn btn-primary"/>
    <ListView for="product in products" class="list-group">
      <v-template>
        <Label :text="product.name + ' - $' + product.price" class="list-group-item"/>
      </v-template>
    </ListView>
  </StackLayout>
</template>

<script>
export default {
  data() {
    return {
      products: [],
      newProduct: {
        name: "",
        price: ""
      }
    };
  },
  methods: {
    addProduct() {
      if (this.newProduct.name.trim() && this.newProduct.price) {
        this.products.push({...this.newProduct});
        this.newProduct.name = "";
        this.newProduct.price = "";
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

<template>
  <header>
    <nav class="navbar navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">FastAPI + Vue</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarCollapse"
          aria-controls="navbarCollapse"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse show navbar-collapse side-nav" id="navbarCollapse">
          <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Listado de resultados</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/upload">Carga de resultados</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile"
                >Mi perfil</router-link
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" @click="logout">Cerrar sesión</a>
            </li>
          </ul>
          <ul v-else class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/register"
                >Registrarse</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Iniciar sesión</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { defineComponent } from "vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.esm.min.js";

export default defineComponent({
  name: "NavBar",
  data() {
    return {
      show: false,
    };
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch("logOut");
      this.$router.push("/login");
    },
  },
});
</script>

<style scoped>
a {
  cursor: pointer;
}

.bg-dark {
  background-color: #6a42ff !important;
}
</style>

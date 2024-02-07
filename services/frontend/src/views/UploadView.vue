<template>
  <div>
    <section>
      <h1>Subir nuevo resultado</h1>
      <hr />
      <br />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="patient_name" class="form-label"
            >Nombre del paciente:</label
          >
          <input
            type="text"
            name="patient_name"
            v-model="form.patient_name"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Tipo de resultado:</label>
          <select name="type" v-model="form.type" class="form-control" required>
            <option value="0">Positivo</option>
            <option value="1">Negativo</option>
            <option value="2">Insuficiente</option>
            <option value="3">Cancelado</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="gen" class="form-label">Gen:</label>
          <textarea
            name="gen"
            v-model="form.gen"
            class="form-control"
            maxlength="20"
            required
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </section>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { mapGetters, mapActions } from "vuex";

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Upload",
  data() {
    return {
      form: {
        patient_name: "",
        type: 0,
        gen: "",
      },
    };
  },
  created: function () {
    return this.$store.dispatch("getNotes");
  },
  computed: {
    ...mapGetters({ notes: "stateNotes" }),
  },
  methods: {
    ...mapActions(["createNote"]),
    async submit() {
      await this.createNote(this.form);
      this.form.patient_name = "";
      this.form.type = 0;
      this.form.gen = "";
    },
  },
});
</script>

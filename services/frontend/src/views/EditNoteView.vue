<template>
  <section>
    <h1>Editar resultado</h1>
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
        <label for="type" class="form-label">Tipo:</label>
        <select v-model="form.type" id="type" class="form-control" required>
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
</template>

<script>
import { defineComponent } from "vue";
import { mapGetters, mapActions } from "vuex";

export default defineComponent({
  name: "EditNote",
  props: ["id"],
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
    this.GetNote();
  },
  computed: {
    ...mapGetters({ note: "stateNote" }),
  },
  methods: {
    ...mapActions(["updateNote", "viewNote"]),
    async submit() {
      try {
        let note = {
          id: this.id,
          form: this.form,
        };
        await this.updateNote(note);
        this.$router.push({ name: "Note", params: { id: this.note.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async GetNote() {
      try {
        await this.viewNote(this.id);
        this.form.patient_name = this.note.patient_name;
        this.form.type = this.note.type;
        this.form.gen = this.note.gen;
      } catch (error) {
        console.error(error);
        this.$router.push("/upload");
      }
    },
  },
});
</script>

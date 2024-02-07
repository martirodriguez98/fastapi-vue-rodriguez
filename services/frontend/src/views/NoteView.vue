<template>
  <div v-if="note">
    <p><strong>Paciente:</strong> {{ note.patient_name }}</p>
    <p><strong>Doctor:</strong> {{ note.author.username }}</p>
    <p><strong>Tipo:</strong> {{ getTypeText(note.type) }}</p>
    <p><strong>Gen:</strong> {{note.gen}} </p>

    <div v-if="user.id === note.author.id">
      <p><router-link :to="{name: 'EditNote', params:{id: note.id}}" class="btn btn-primary">Edit</router-link></p>
      <p><button @click="removeNote()" class="btn btn-secondary">Delete</button></p>
    </div>
  </div>
</template>


<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Note',
  props: ['id'],
  async created() {
    try {
      await this.viewNote(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push('/upload');
    }
  },
  computed: {
    ...mapGetters({ note: 'stateNote', user: 'stateUser'}),
  },
  methods: {
    ...mapActions(['viewNote', 'deleteNote']),
    async removeNote() {
      try {
        await this.deleteNote(this.id);
        this.$router.push('/upload');
      } catch (error) {
        console.error(error);
      }
    }, 
    getTypeText: function (type) {
      switch (type) {
        case 0:
          return "Positivo";
        case 1:
          return "Negativo";
        case 2:
          return "Insuficiente";
        case 3:
          return "Cancelado";
        default:
          return "-";
      }
    },
  },
});
</script>

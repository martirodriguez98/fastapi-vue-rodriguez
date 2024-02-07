<template>
  <div v-if="isLoggedIn">
    <section>
      <h1>Estadísticas</h1>
      <hr />
      <br />
      <div class="row">
        <div class="col-md-4">
          <h3>Cantidad de estudios positivos</h3>
        </div>
        <div class="col-md-4">
          <h3>Positivos por gen</h3>
        </div>
        <div class="col-md-4">
          <h3>
            Resultados cargados por {{ stateUser && stateUser.full_name }}
          </h3>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <p>Excluyendo cancelados e insuficientes</p>
          <p>Total: {{ positives_count }} - {{ positives_percentage }}%</p>
        </div>
        <div class="col-md-4">
          <p>Excluyendo cancelados e insuficientes</p>
          <ul>
            <li v-for="(count, gen) in positive_by_gen" :key="gen">
              {{ gen }}: {{ count }}
            </li>
          </ul>
        </div>
        <div class="col-md-4">
          <p>Incluyendo todo tipo de resultado</p> 
          <p>Total: {{ this.notes_by_user }} - {{ this.notes_by_user_percentage }}%</p>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <CanvasJSChart
            :options="positivesPieChartOptions"
            @chart-ref="positivesPieChart"
            :styles="{ width: '100%', height: '100px' }"
            :key="JSON.stringify(positivesPieChartOptions)"
          />
        </div>
        <div class="col-md-4">
          <CanvasJSChart
            :options="positiveByGenOptions"
            @chart-ref="positiveByGenChart"
            :styles="{ width: '100%', height: '100px' }"
            :key="JSON.stringify(positiveByGenOptions)"
          />
        </div>
        <div class="col-md-4">
          <CanvasJSChart
            :options="notesByUserOptions"
            @chart-ref="notesByUserChart"
            :styles="{ width: '100%', height: '100px' }"
            :key="JSON.stringify(notesByUserOptions)"
          />
        </div>
      </div>

    </section>

    <section>
      <br />
      <h1>Resultados</h1>
      <hr />
      <br />

      <div v-if="isLoggedIn && notes && notes.length" class="row">
        <div v-for="note in notes" :key="note.id" class="col-md-4">
          <div class="card" style="width: 18rem">
            <div class="card-body">
              <ul>
                <li><strong>Paciente:</strong> {{ note.patient_name }}</li>
                <li><strong>Doctor:</strong> {{ note.author.username }}</li>
                <li>
                  <strong>Resultado:</strong> {{ getTypeText(note.type) }}
                </li>
                <li><strong>Gen:</strong> {{ note.gen }}</li>
              </ul>
              <div style="text-align: center">
                <button class="btn btn-primary" @click="viewNote(note.id)">
                  View
                </button>
              </div>
            </div>
          </div>
          <br />
        </div>
      </div>

      <div v-else>
        <p>Nothing to see. Check back later.</p>
      </div>
    </section>
  </div>
  <div v-else>
    <p>You must be logged to see this page</p>
    <p>
      <span><a href="/register">Register</a></span>
      <span> or </span>
      <span><a href="/login">Log In</a></span>
    </p>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { mapGetters, mapActions } from "vuex";

export default defineComponent({
  name: "HomeComponent",
  data() {
    return {
      form: {
        patient_name: "",
        type: 0,
        gen: "",
      },
      user: null,
      positives_count: 0,
      positives_percentage: 0.0,
      negatives_count: 0,
      positive_by_gen: null,
      positivesPieChart: null,
      positivesPieChartOptions: {
        animationEnabled: true,
        data: [
          {
            type: "pie",
            responsive: true,
            dataPoints: [
              { label: "Positivos", color: "#8666ab" },
              { label: "Negativos", color: "#d3d3d3" },
            ],
          },
        ],
      },
      positiveByGenChart: {},
      positiveByGenOptions: {
        animationEnabled: true,
        data: [
          {
            type: "column",
            color: "#8666ab",
            responsive: true,
            dataPoints: [],
          },
        ],
      },
      notes_by_user: 0,
      notes_by_user_percentage: 0.0,
      notesByUserChart: {},
      notesByUserOptions: {
        animationEnabled: true,
        data: [
          {
            type: "pie",
            responsive: true,
            dataPoints: [],
          },
        ],
      },
    };
  },

  created: function () {
    return this.$store.dispatch("getNotes").then(() => {
      this.calculatePositives();
      this.positivesPieChartOptions.data[0].dataPoints[0].y =
        this.positives_count;
      this.positivesPieChartOptions.data[0].dataPoints[1].y =
        this.negatives_count;
      this.calculatePositiveByGen();
      this.calculateNotesByUser();
    });
  },

  watch: {
    positives_count(new_value) {
      this.positivesPieChartOptions.data[0].dataPoints[0].y = new_value;
    },

    negatives_count(new_value) {
      this.positivesPieChartOptions.data[0].dataPoints[1].y = new_value;
    },
  },
  computed: {
    ...mapGetters({ notes: "stateNotes" }),
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
    ...mapGetters(["stateUser"]),
  },

  methods: {
    ...mapActions(["createNote"]),
    async submit() {
      await this.createNote(this.form);
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
    calculatePositives: function () {
      const filteredStudies = this.notes.filter(
        (note) => note.type !== 2 && note.type !== 3
      );
      const positiveStudiesCount = filteredStudies.reduce((count, note) => {
        if (note.type === 0) {
          count++;
        }
        return count;
      }, 0);

      this.negatives_count = filteredStudies.reduce((count, note) => {
        if (note.type === 1) {
          count++;
        }
        return count;
      }, 0);

      const totalStudiesCount = filteredStudies.length;
      this.positives_count = positiveStudiesCount;
      this.positives_percentage = (
        (positiveStudiesCount / totalStudiesCount) *
        100
      ).toFixed(2);
    },

    calculatePositiveByGen: function () {
      const positiveByGen = {};
      this.notes.forEach((note) => {
        if (note.type == 0) {
          const gen = note.gen;
          if (!positiveByGen[gen]) {
            positiveByGen[gen] = 1; // Initialize count for this gen
          } else {
            positiveByGen[gen]++; // Increment count for this gen
          }
        }
      });

      this.positiveByGenOptions.data[0].dataPoints = Object.entries(
        positiveByGen
      ).map(([gen, count]) => ({
        label: gen,
        y: count,
      }));

      this.positive_by_gen = positiveByGen;
    },

    calculateNotesByUser: function () {
      this.notes_by_user = this.notes.filter(
        (note) => note.author.username === this.stateUser.username
      ).length;

      this.notes_by_user_percentage = (
        (this.notes_by_user / this.notes.length) *
        100
      ).toFixed(2);

      this.notesByUserOptions.data[0].dataPoints = [
        {
          label: this.stateUser.full_name,
          y: this.notes_by_user,
          color: "#8666ab",
        },
        {
          label: "Otros",
          y: this.notes.length - this.notes_by_user,
          color: "#d3d3d3",
        },
      ];
    },

    viewNote(id) {
      this.$router.push({ name: "Note", params: { id } });
    },
  },
});
</script>
<style>
.btn-primary {
  background-color: #6a42ff;
  border-color: #6a42ff;
}
.btn-primary:hover {
  background-color: #4a2db5;
  border-color: #4a2db5;
}
</style>
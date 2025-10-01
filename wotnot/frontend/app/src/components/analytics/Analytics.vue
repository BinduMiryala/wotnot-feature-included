<template>
  <div class="content-section m-8 md:ml-72">
    <div class="bg-white rounded-lg rounded-[14px] border border-[#cccccc] max-w-[800px] p-4">

      <div class="flex justify-between items-center">
        <div>
          <h2 class="title">Conversations <span class="info">Info</span></h2>
        </div>

        <!-- <label>Start Date: <input type="date" v-model="startDate" /></label>
        <label>End Date: <input type="date" v-model="endDate" /></label> -->

        <div class="flex items-center ml-auto justify-end">
          <el-date-picker v-model="dateRange" type="daterange" range-separator="to" start-placeholder="Start date"
            end-placeholder="End date" value-format="YYYY-MM-DD" @change="updateDates"  class="max-w-[100%] mr-2 "/>

          <button @click="fetchAnalyticsData"
          class="relative h-auto w-auto p-1 text-[15px]  border-solid  text-white  bg-blue-500 hover:bg-blue-700">Apply</button>
        </div>
      </div>



      <div v-if="error" class="error">{{ error }}</div>

      <canvas ref="analyticsChart"></canvas>
    </div>

  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import "element-plus/dist/index.css";

export default {
  name: "dataAnalytics",
  data() {
    return {

      apiUrl: process.env.VUE_APP_API_URL,
      dateRange: [],
      startDate: '',
      endDate: '',
      analyticsData: null,
      error: null,
      loading: false,
      chart: null,
      chartLabels: [],
      chartData: {
        sent: [],
        delivered: []
      }
    };
  },
  created() {
    // Get today's date
    const today = new Date();
    this.endDate = today.toISOString().split("T")[0]; // Format as YYYY-MM-DD

    // Get date 7 days ago
    const lastWeek = new Date();
    lastWeek.setDate(today.getDate() - 7);
    this.startDate = lastWeek.toISOString().split("T")[0];// Format as YYYY-MM-DD

    this.fetchAnalyticsData();
    this.renderChart();
  },
  methods: {

    updateDates() {
      this.startDate = this.dateRange ? this.dateRange[0] : null;
      this.endDate = this.dateRange ? this.dateRange[1] : null;
    },
    fetchAnalyticsData() {
      if (!this.startDate || !this.endDate) {
        this.error = "Start and end dates are required.";
        return;
      }

      this.loading = true;
      this.error = null;
      this.chartLabels = [];
      this.chartData = {
        sent: [],
        delivered: []
      };

      const url = `${this.apiUrl}/get-analytics?start=${this.startDate}&end=${this.endDate}`;

      fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}` // Example for auth token
        }
      })
        .then(res => {
          if (!res.ok) throw new Error("Failed to fetch analytics");
          return res.json();
        })
        .then(data => {
          this.analyticsData = data;

          const rawData = data.analytics?.data_points || [];
          if (rawData.length === 0) {
            this.error = "No analytics data found.";
            return;
          }

          let sampledData = rawData;

          // If we have more than 10 data points, sample them evenly
          if (rawData.length > 10) {
            const interval = Math.ceil(rawData.length / 10);
            sampledData = rawData.filter((_, index) => index % interval === 0);
          }

          sampledData.forEach(item => {
            const date = new Date(item.start * 1000);
            const formattedDate = date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }); // Example: "20 Mar"
            this.chartLabels.push(formattedDate);
            this.chartData.sent.push(item.sent || 0);
            this.chartData.delivered.push(item.delivered || 0);
          });
          // rawData.forEach(item => {
          //   const date = new Date(item.start * 1000);
          //   const formattedDate = date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }); // e.g., "20 Mar"
          //   this.chartLabels.push(formattedDate);
          //   this.sentData.push(item.sent);
          //   this.deliveredData.push(item.delivered);
          // });

          this.renderChart();
        })
        .catch(err => {
          this.error = err.message;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    renderChart() {
      const ctx = this.$refs.analyticsChart;

      if (this.chart) {
        this.chart.destroy();
      }

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.chartLabels,
          datasets: [
            {
              label: 'not delivered',
              data: this.chartData.sent.map((val, index) => val - this.chartData.delivered[index]),
              borderColor: 'Red',
              backgroundColor: 'rgba(123, 97, 255, 0.2)',
              borderDash: [5, 5],
              tension: 0
            },
            {
              label: 'Sent',
              data: this.chartData.sent,
              borderColor: '#7B61FF',
              backgroundColor: 'rgba(123, 97, 255, 0.2)',
              borderDash: [],
              tension: 0
            },
            {
              label: 'Delivered',
              data: this.chartData.delivered,
              borderColor: '#00C2D7',
              backgroundColor: 'rgba(0, 194, 215, 0.2)',
              borderDash: [5, 5],
              tension: 0
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top'
            },
            title: {
              display: true,
              text: 'All Conversations (Sent & Delivered)'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Messages'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: black;
}

.info {
  font-size: 0.9rem;
  color: #1486ff;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 10px;
}

canvas {
  max-width: 100%;
  margin-top: 30px;
}
</style>

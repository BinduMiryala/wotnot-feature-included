<template>
    <div class="cost-summary">
      <h2 class="title">Cost Summary <span class="info">Info</span></h2>
  
      <div class="grid-container">
        <!-- Left Top: Month-to-date cost -->
        <div class="grid-item">
          <h3>Month-to-date cost</h3>
          <p class="cost"><u>₹{{ monthToDateCost }}</u></p>
          <p class="change">
            <span :class="monthToDateChangeClass">{{ monthToDateChange }}</span>% compared to last month for same period
          </p>
        </div>
  
        <!-- Right Top: Last month's cost for same period -->
        <div class="grid-item">
          <h3>Last month’s cost for same time period</h3>
          <p class="cost"><u>₹{{ lastMonthSamePeriodCost }}</u></p>
          <p class="date-range">{{ lastMonthDateRange }}</p>
        </div>
  
        <!-- Left Bottom: Forecasted cost -->
        <div class="grid-item">
          <h3>Total forecasted cost for current month</h3>
          <p class="cost"><u>₹{{ forecastedCost }}</u></p>
          <p class="change">
            <span :class="forecastChangeClass">{{ forecastChange }}</span>% compared to last month's total costs
          </p>
        </div>
  
        <!-- Right Bottom: Last month's total cost -->
        <div class="grid-item">
          <h3>Last month’s total cost</h3>
          <p class="cost"><u>₹{{ lastMonthTotalCost }}</u></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import axios from "axios";
import dayjs from "dayjs";

export default {
  data() {
    return {

      apiUrl: process.env.VUE_APP_API_URL,

      monthToDateCost: 0,
      monthToDateChange: "",
      monthToDateChangeClass: "",
      lastMonthSamePeriodCost: 0,
      lastMonthDateRange: "",
      forecastedCost: 0,
      forecastChange: "",
      forecastChangeClass: "",
      lastMonthTotalCost: 0,
    };
  },
  methods: {
    async fetchAnalyticsData() {
      try {
        const response = await axios.get(`${this.apiUrl}/conversation-cost-history/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        console.log("Raw API Response:", response.data); // Debugging Step

        const data = response.data.conversation_analytics;
        if (!data || data.length === 0) {
          console.warn("No conversation data available.");
          return;
        }

        this.processData(data);
      } catch (error) {
        console.error("Error fetching analytics:", error);
      }
    },

    processData(data) {
      const currentMonth = dayjs().format("YYYY-MM"); // e.g., "2025-03"
      const lastMonth = dayjs().subtract(1, "month").format("YYYY-MM"); // e.g., "2025-02"
      const today = dayjs().date(); // Get today's day in the month

      let monthToDateCost = 0;
      let lastMonthSamePeriodCost = 0;
      let lastMonthTotalCost = 0;
      let totalDaysLastMonth = dayjs().subtract(1, "month").daysInMonth();

      data.forEach((entry) => {
        const entryMonth = dayjs(entry.start_time).format("YYYY-MM");
        const entryDay = dayjs(entry.start_time).date();

        if (entryMonth === currentMonth) {
          monthToDateCost += entry.cost;
        }
        if (entryMonth === lastMonth) {
          lastMonthTotalCost += entry.cost;
          if (entryDay <= today) {
            lastMonthSamePeriodCost += entry.cost;
          }
        }
      });



      this.monthToDateCost = parseFloat(monthToDateCost.toFixed(2));
this.lastMonthSamePeriodCost = parseFloat(lastMonthSamePeriodCost.toFixed(2));
this.lastMonthTotalCost = parseFloat(lastMonthTotalCost.toFixed(2));
this.monthToDateChange = parseFloat(((monthToDateCost - lastMonthSamePeriodCost) / (lastMonthSamePeriodCost || 1) * 100).toFixed(2));
this.forecastedCost = parseFloat(((monthToDateCost / today) * totalDaysLastMonth).toFixed(2));
this.forecastChange = parseFloat(((this.forecastedCost - lastMonthTotalCost) / (lastMonthTotalCost || 1) * 100).toFixed(2));
this.forecastChangeClass = data.forecast_change > 0 ? "up" : "down";
this.monthToDateChangeClass = monthToDateCost > lastMonthSamePeriodCost ? "up" : "down";
// Log AFTER updating values
console.log("Processed Summary Data:", {
  monthToDateCost: this.monthToDateCost,
  monthToDateChange: this.monthToDateChange,
  lastMonthSamePeriodCost: this.lastMonthSamePeriodCost,
  lastMonthTotalCost: this.lastMonthTotalCost,
  forecastedCost: this.forecastedCost,
  forecastChange: this.forecastChange,
});

    },
  },
  mounted() {
    this.fetchAnalyticsData();
  },
};
</script>

  
  
  
  <style scoped>
  .cost-summary {
    padding: 20px;
    font-family: Arial, sans-serif;

  }
  .title {
    font-size: 1.5rem;
    font-weight: bold;
    color:black;
  }
  .info {
    font-size: 0.9rem;
    color: #1a73e8;
    cursor: pointer;
  }
  .grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }
  .grid-item {
    padding: 5px;
    border-radius: 5px;
  }
  .cost {
    font-size: 20px;
    font-weight: bold;
    color: #1a73e8;
  }
  .change {
    font-size: 0.9rem;
  }
  .up {
    color: green;
  }
  .down {
    color: red;
  }
  .date-range {
    font-size: 0.8rem;
    color: gray;
  }
  </style>
  
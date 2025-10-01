<template>

    <div class="cost-summary">
        <h2 class="title">Cost Breakdown <span class="info">Info</span></h2>
        <canvas ref="chartCanvas"></canvas>
    </div>

</template>



<script>
import { ref, onMounted } from "vue";
import axios from "axios";

import {
    Chart,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
} from "chart.js";


// Register Chart.js components
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default {



    setup() {
        const chartCanvas = ref(null);
        let chartInstance = null;
        const apiUrl = process.env.VUE_APP_API_URL ||import.meta.env.VITE_API_URL ;

        const fetchData = async () => {
            try {
                const response = await axios.get(`${apiUrl}/conversation-cost-history/`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                });

                console.log("API Response:", response.data);

                const data = response.data.conversation_analytics;
                const monthlyData = {};

                // Process and aggregate data
                data.forEach((item) => {
                    const date = new Date(item.start_time);
                    const month = date.toLocaleString("default", { month: "short", year: "numeric" }); // "Mar 2025"

                    if (!monthlyData[month]) {
                        monthlyData[month] = { MARKETING: 0, UTILITY: 0 };
                    }
                    monthlyData[month][item.conversation_category] += item.cost;
                });

                console.log("Processed Monthly Data:", monthlyData);

                // Sort months correctly
                const sortedMonths = Object.keys(monthlyData)
                    .map((month) => ({ month, date: new Date(month) }))
                    .sort((a, b) => a.date - b.date)
                    .map((entry) => entry.month);

                // Keep only the last 4 months
                const latestMonths = sortedMonths.slice(-4);

                // Extract data for datasets
                const marketingData = latestMonths.map((month) => monthlyData[month]?.MARKETING || 0);
                const utilityData = latestMonths.map((month) => monthlyData[month]?.UTILITY || 0);

                // Render the chart
                renderChart(latestMonths, marketingData, utilityData);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        const renderChart = (labels, marketingData, utilityData) => {
            if (chartInstance) {
                chartInstance.destroy(); // Destroy previous chart instance if exists
            }

            const ctx = chartCanvas.value.getContext("2d");

            chartInstance = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Marketing",
                            backgroundColor: "#7B61FF",
                            data: marketingData,
                            stack: "stack1",
                        },
                        {
                            label: "Utility",
                            backgroundColor: "red",
                            data: utilityData,
                            stack: "stack1",
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true },
                        title: { display: true, text: "Cost Breakdown (Last 4 Months)" },
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false, // Remove vertical grid lines
                            },
                            stacked: true,
                        },
                        y: {
                            grid: {
                                drawBorder: false,
                                drawTicks: false,
                                color: function (context) {
                                    return context.tick.value === 0 ? "transparent" : "#cccccc"; // Show only horizontal lines
                                },
                            },
                            stacked: true,
                        },
                    },
                    elements: {
                        bar: {
                            barThickness: 20,
                        },
                    },
                },
            });
        };



        onMounted(fetchData);

        return { chartCanvas };
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
    color: black;
}

.info {
    font-size: 0.9rem;
    color: #1486ff;
    cursor: pointer;
}

.chart-container {
    width: 30%;

}

/* Custom scrollbar for table overflow */
.custom-scrollbar::-webkit-scrollbar {
    width: 10px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #888;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Responsive Table Styles */
@media (max-width: 768px) {
    table thead {
        display: none;
    }

    table tbody tr {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
        border-bottom: 2px solid #ddd;
    }

    table tbody tr td {
        display: block;
        text-align: right;
        position: relative;
        padding-left: 50%;
    }

    table tbody tr td::before {
        content: attr(data-label);
        position: absolute;
        left: 0;
        padding-left: 10px;
        font-weight: bold;
        text-transform: uppercase;
    }
}
</style>

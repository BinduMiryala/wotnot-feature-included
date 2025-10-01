<template>
    <div class="content-section m-8 md:ml-72">

      <div class="rounded-lg mb-4 rounded-[14px] bg-white border border-[#cccccc]">
        <CostSummary />
      </div>

      <div class="grid grid-cols-[45%_54%] gap-4">
        <!-- Left Grid -->
        <div class="bg-white rounded-lg rounded-[14px] border border-[#cccccc]">
          <CostBarChart/>
        </div>
      
        <!-- Right Grid -->
        <div class="bg-white rounded-lg rounded-[14px] border border-[#cccccc]">
          <PurchaseHistory/>
        </div>
      </div>
    
    </div>

</template>


<script>
import CostSummary from "./costSummary.vue";
import CostBarChart from "./costBarChart.vue";
import PurchaseHistory from "./PurchaseHistory.vue";

export default {
  components:{
      CostSummary,CostBarChart,PurchaseHistory
  }
};
</script>


<style scoped>


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

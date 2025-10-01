<template>
  <div class="content-section m-8 md:ml-72">

    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-2xl font-bold ">Woocommerce</h2>
        <p>Integrate Wotnot with Woocommerce</p>
      </div>

      <div >
        <!-- <button @click="showPopup = true"
          class="text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base w-full md:w-auto">
          + Create Integration
        </button> -->
        <button class="bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-green-800"
        @click="showPopup = true">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
          </svg>
          Create Integration
      </button>
      </div>
    </div>

    <div class="flex-col  md:flex-row justify-between mb-4 border-b pb-5">
      <div class="woocommerce-card p-4 bg-[#f8f9fa] rounded-lg shadow-md max-w-sm  pb-5">
        <div class="flex items-center mb-4">
          <img src="@/assets/woocommerce.png" alt="WooCommerce Logo" class="rounded-full h-12 w-12" />
          <h2 class="text-xl font-semibold ml-4">WooCommerce</h2>
        </div>
        <p class="text-sm font-medium text-gray-500 mb-2">
          Status:
          <span :class="status === 'connected' ? 'text-green-500' : 'text-red-500'">
            {{ status }}
          </span>
        </p>
        <p class="text-sm text-gray-600 mb-4">
          Boost your cart recovery & reengage with your customers to upsell
        </p>
        <button @click="showWooStoreSetupPopup = true"
          class="bg-green-600 text-white text-sm font-semibold py-2 px-4 rounded-lg hover:bg-green-700 flex items-center">
          Store Setup →
        </button>
      </div>

    </div>



    <PopUp1 v-if="showWooStoreSetupPopup" @close="showWooStoreSetupPopup = false"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">

      <label class="block text-gray-700 font-semibold mb-2">Store Name<span class="text-red-800">*</span></label>
      <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="store_name"
        :disabled="status == 'connected'" :class="{ 'text-gray-400': status === 'connected' }">

      <label class="block text-gray-700 font-semibold mb-2">REST API Key<span class="text-red-800">*</span></label>
      <input type="text" id="APIkey" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIkey"
        placeholder="Enter your REST API key" :disabled="status == 'connected'"
        :class="{ 'text-gray-400': status === 'connected' }">

      <label class="block text-gray-700 font-semibold mb-2">REST API Secret<span class="text-red-800">*</span></label>
      <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIsecret"
        placeholder="Enter your REST API secret" :disabled="status == 'connected'"
        :class="{ 'text-gray-400': status === 'connected' }">

      <label class="block text-gray-700 font-semibold mb-2">Woocommerce Base URL<span
          class="text-red-800">*</span></label>
      <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="Base_url"
        :disabled="status == 'connected'" :class="{ 'text-gray-400': status === 'connected' }">

      <div class="flex justify-end pt-3 items-center justify-between" v-if="status != 'connected'">
        <p>Status: <span :class="status === 'connected' ? 'text-green-500' : 'text-red-500'">
            {{ status }}
          </span></p>
        <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded"
          @click="testWooCommerceConnection">Connect</button>
      </div>

      <div class="flex justify-end pt-3 items-center justify-between" v-else>
        <p> Status: <span :class="status === 'connected' ? 'text-green-500' : 'text-red-500'">
            {{ status }}
          </span></p>
        <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded"
          @click="disconnectWooCommerce">Disconnect</button>

      </div>

      <div>

      </div>




    </PopUp1>

    <!-- <div class="woocommerceBox cursor-pointer p-4  hover:bg-gray-300 rounded-lg mb-4">
      <img src="@/assets/woocommerce.png" alt="Woocommerce" @click="showPopup = true">
    </div> -->

    <PopUp1 v-if="showPopup" @close="closePopup"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">
      <h2 class="text-xl font-bold ">Woocommerce Integration</h2>
      <hr class="mb-4" />
      <div class="popup-content custom-scrollbar p-4">
        <form class="space-y-4" @submit.prevent="submitIntegrationForm(this.SelectedAction)" :class="{ 'opacity-50 pointer-events-none': isSubmitted }">



          <div>
            <label class="block text-gray-700 font-semibold mb-2" required>Select action<span
                class="text-red-800">*</span></label>
            <select v-model="SelectedAction"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your option</option>
              <option value="woo/order_confirmation">Send Order Confirmation</option>
              <option value="Abandoned Cart">Abandoned Cart</option>
              <option value="woo/pwn">PWNs (Pre Webinar Notifications)</option>
            </select>
          </div>


          <div v-if="SelectedAction === 'woo/order_confirmation'">


            <label for="description" class="block text-gray-700 font-semibold mb-2">Description
              <span class="text-red-800">*</span>
            </label>
            <input type="text" id="description" v-model="integration_description"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400">


            <label class="block text-gray-700 font-semibold mb-2">Select template<span
                class="text-red-800">*</span></label>
            <select v-model="selectedTemplate" @change="onTemplateSelect"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option v-for="template in templates" :key="template.id" :value="template">
                {{ template.name }}
              </option>
            </select>

            <div v-if="selectedTemplate !== null">

              <div v-if="selectedTemplateHasImage">
                <label for="" class="block text-sm font-semibold">Upload Media</label>
                <input type="file" @change="onFileChange" class="mb-2 w-[60%] mr-1" required>
              </div>
              <div v-if="uploadedMedia">{{ this.mediaId }}</div>

              <label for="" class="block text-gray-400 font-semibold mb-2">Add Parameter (if any)<span
                  class="text-red-800"></span></label>
              <div v-for="(parameter, index) in parameters" :key="index" class="flex items-center space-x-2 mb-2">

                <select v-model="parameter.key" class="w-full p-2 border rounded-md bg-gray-100">
                  <option value="" disabled>Select your parameter</option>
                  <option v-for="option in parameterOptions" :key="option" :value="option.key">{{ option.label }}
                  </option>
                </select>

                <button @click.prevent="removeParameter(index)"
                  class="relative my-2 h-8 w-24 border-2 border-solid border-red-500 text-red-500 hover:text-gray-200 hover:bg-red-700">
                  Remove
                </button>
              </div>
              <button @click.prevent="addParameter"
                class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">
                Add Parameter
              </button>

              <!-- Searchable Select using vue-select -->
              <label class="block text-gray-700 font-semibold mb-2">Select product<span
                  class="text-red-800">*</span></label>
              <vue3-select v-model="productID" :options="products" label="name" :reduce="product => product.id"
                placeholder="Search products..." required />
              <p :style="{ color: 'gray', fontSize: '12px' }"> Selected Product ID: {{ productID }}</p>

              <h3 class="text-lg font-bold mb-2">Woocommerce Setup</h3>
              <input type="text" v-model="webhookLink" class="w-full p-2 border rounded-md bg-gray-100" disabled>

              <ul class="list-disc pl-5 mt-4 space-y-2 text-sm">
                <li>Navigate to <b>WooCommerce > Settings</b></li>
                <li>Click on the <b>Advanced tab</b></li>
                <li>In the <b>Advanced settings</b>, click on <b>Webhook</b></li>
                <li>Click the <b>Add Webhook</b> button.</li>
                <li><b>Configure Webhook Settings</b></li>
                <li><b>Name</b>: Give your webhook a name to identify it.</li>
                <li><b>Status:</b> Set this to Active.</li>
                <li>Topic: Choose the event you want the webhook to listen to</li>
                <li><b>Delivery URL: use the above given webhook URL</b></li>
                <li><b>Secret:</b> leave blank</li>
                <li><b>API Version:</b> Leave the default version</li>
                <li>Click Save Webhook to activate the integration</li>
              </ul>



            </div>
          </div>

          <div v-if="SelectedAction === 'woo/pwn'">

            <label for="description" class="block text-gray-700 font-semibold mb-2">Description
              <span class="text-red-800">*</span>
            </label>
            <input type="text" id="description" v-model="integration_description"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400">

            <label class="block text-gray-700 font-semibold mb-2">Select template<span
                class="text-red-800">*</span></label>
            <select v-model="selectedTemplate" @change="onTemplateSelect"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your template</option>
              <option v-for="template in templates" :key="template.id" :value="template">{{ template.name }}</option>
            </select>



            <div v-if="selectedTemplate !== null">

              <div v-if="selectedTemplateHasImage">
                <label for="" class="block text-sm font-semibold">Upload Media</label>
                <input type="file" @change="onFileChange" class="mb-2 w-[60%] mr-1" required>
              </div>
              <div v-if="uploadedMedia">{{ this.mediaId }}</div>
            

              <div v-for="(parameter, index) in parameters" :key="index" class="flex items-center space-x-2 mb-2">

                <select v-model="parameter.key" class="w-full p-2 border rounded-md bg-gray-100">
                  <option value="" disabled>Select your parameter</option>
                  <option v-for="option in parameterOptions" :key="option" :value="option.key">{{ option.label }}
                  </option>
                </select>
                <button @click.prevent="removeParameter(index)"
                  class="relative my-2 h-8 w-24 border-2 border-solid border-red-500 text-red-500 hover:text-gray-200 hover:bg-red-700">
                  Remove
                </button>
              </div>

              <label class="block text-gray-500 font-semibold mb-2">Add parameter (if any)<span
                  class="text-red-800">*</span></label>
              <button @click.prevent="addParameter"
                class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">
                Add Parameter
              </button>


              <!-- <label class="block text-gray-700 font-semibold mb-2">REST API Key<span
                  class="text-red-800">*</span></label>
              <input type="text" id="APIkey" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIkey"
                placeholder="Enter your REST API key">

              <label class="block text-gray-700 font-semibold mb-2">REST API Secret<span
                  class="text-red-800">*</span></label>
              <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIsecret"
                placeholder="Enter your REST API secret"> -->


                <label class="block text-gray-700 font-semibold mb-2">Execution Time and Days<span
                  class="text-red-800">*</span></label>
              <div class="bg-[#f5f6fa] items-center space-x-2 p-2 justify-between">

                <div class="flex items-center ">

                  <div class="mr-2">
                    <label for="scheduleTime" class="block text-sm font-medium">Time<span
                        class="text-red-800">*</span> (in IST)</label>
                    <input type="time" v-model="scheduleTime" id="scheduleTime" required
                      class="border border-gray-300 rounded px-3 py-2 w-full">
                  </div>


                  <div class="flex justify-between items-center mt-4">
                    <div v-for="day in days" :key="day.id" @click="toggleDaySelection(day.id)" :class="[
                      'w-10 h-10 flex items-center justify-center cursor-pointer rounded-full font-bold transition-all duration-200',
                      day.selected ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700',
                    ]">
                      {{ day.initial }}
                    </div>
                  </div>

                  <!-- <p class="mt-4 text-gray-700 font-medium">
                    Selected days: {{ selectedDays.join(", ") }}
                  </p> -->
                </div>
              </div>

              <label class="block text-gray-700 font-semibold mb-2">Filter Contacts by</label>

              <div class="bg-[#f5f6fa] items-center space-x-2 p-2 justify-between">

                <label class="block text-sm font-medium">Date Range<span class="text-red-800">*</span></label>

                <div class="flex items-center space-x-2">
                  <div class="mb-4">
                    <input type="date" id="startDate" v-model="startDate"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required />
                  </div>

                  <p>to</p>

                  <div class="mb-4">
                    <input type="date" id="endDate" v-model="endDate"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required />
                  </div>
                </div>
              </div>


              <div class="bg-[#f5f6fa] items-center space-x-2 p-2 justify-between">

                <label for="Product" class="block text-sm font-medium">Product<span class="text-red-800">*</span></label>

                <vue3-select id="Product" v-model="productID" :options="products" label="name" :reduce="product => product.id"
                  placeholder="Search products..." />
                <p :style="{ color: 'gray', fontSize: '12px' }"> Selected Product ID: {{ productID }}</p>

              </div>

              <!-- Searchable Select using vue-select -->

              <div class="bg-[#f5f6fa] items-center space-x-2 p-2 justify-between">

                <label for="orderStatus" class="block text-sm font-medium">Order Status<span class="text-red-800">*</span></label>

                <multiselect id="orderStatus" v-model="selectedStatuses" :options="statuses" :multiple="true" :close-on-select="false"
                  :clear-on-select="false" placeholder="Select order statuses" label="label" track-by="value"
                  class="mt-2" required />

              </div>

            </div>
          </div>




          
          <button
          type="submit"
          class="bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-green-800"
          :disabled="PopupLoading || isSubmitted">
          <span v-if="PopupLoading"
            class="animate-spin border-2 border-white border-t-transparent rounded-full w-4 h-4 mr-2"></span>
          {{ isSubmitted ? "Submitted" : PopupLoading ? "Submitting..." : "Submit" }}
        </button>

        </form>
      </div>


    </PopUp1>
    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Integration List</b></h3>
   <div class="overflow-x-auto max-h-[32vh] custom-scrollbar">
      <table class="w-full border border-gray-300 rounded-lg text-sm md:text-base bg-white">
        <thead>
          <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
            <th class="p-3 md:p-4 text-center border border-gray-300 sticky top-0 z-10 bg-gray-100">ID</th>
            <th class="p-3 md:p-4 text-center border border-gray-300 sticky top-0 z-10 bg-gray-100">Description</th>
            <th class="p-3 md:p-4 text-center border border-gray-300 sticky top-0 z-10 bg-gray-100">Type</th>
            <th class="p-3 md:p-4 text-center border border-gray-300 sticky top-0 z-10 bg-gray-100">Template</th>
            <th class="p-3 md:p-4 text-center border border-gray-300 sticky top-0 z-10 bg-gray-100">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="integration in integrations" :key="integration.id" class="hover:bg-gray-50">
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ integration.id }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ integration.description }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ integration.type }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ integration.template }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <div class="flex justify-center">
                <button @click="deleteIntegration(integration.integration_id)"
                  class="hover:bg-white rounded-full p-2 transition">
                  <lord-icon src="https://cdn.lordicon.com/skkahier.json"
                    colors="primary:#ff5757,secondary:#000000" trigger="hover"
                    style="width:32px;height:32px">
                  </lord-icon>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>



  </div>
</template>


<script>
import PopUp1 from "../popups/popup1";

import { useToast } from 'vue-toastification';
import axios from "axios";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";
import Vue3Select from 'vue3-select';
import 'vue3-select/dist/vue3-select.css';


export default {


  name: 'AppIntegration',
  data() {

    return {

      apiUrl: process.env.VUE_APP_API_URL,
      // popup
      showPopup: false,
      showWooStoreSetupPopup: false,



      SelectedAction: null,
      templates: [],
      selectedTemplate: null,
      webhookLink: '',
      integrations: [],
      templateParams: [],
      parameters: [],  // List of parameters for the template
      parameterOptions: [{ label: "Customer Name", key: "billing.first_name" },
      // { label: "Order ID", key: "id" },
      // { label: "Order Total", key: "total" },
      // { label: "Customer Phone", key: "billing.phone" },
      // { label: "Payment Method", key: "payment_method" },
    ],

      parameterFields: [{ selected: '' }],
      days: [
        { id: 1, name: "Monday", initial: "M", selected: false },
        { id: 2, name: "Tuesday", initial: "T", selected: false },
        { id: 3, name: "Wednesday", initial: "W", selected: false },
        { id: 4, name: "Thursday", initial: "T", selected: false },
        { id: 5, name: "Friday", initial: "F", selected: false },
        { id: 6, name: "Saturday", initial: "S", selected: false },
        { id: 7, name: "Sunday", initial: "S", selected: false },
      ],


      // woocommerce
      wooAPIsecret: null,
      wooAPIkey: null,
      Base_url: "https://",
      store_name: null,
      connectionStatus: null,


      // woocommerce pwn integration
      scheduleTime:null,
      startDate: null,
      endDate: null,
      productID: null,
      OrderStatus: null,
      statuses: [
        { value: "pending", label: "Pending Payment" },
        { value: "processing", label: "Processing" },
        { value: "on-hold", label: "On Hold" },
        { value: "completed", label: "Completed" },
        { value: "cancelled", label: "Cancelled" },
        { value: "refunded", label: "Refunded" },
        { value: "failed", label: "Failed" },
      ],
      selectedStatuses: [], // Array to hold selected values
      // String to store comma-separated values
      products: [],
      integration_description: null,
      selectedTemplateHasImage:false,
      imageUrl:'',
      media_id:'',



      // Check integration status
      statusMessage: "", // Message from the API
      error: null, // Error message if any

      isSubmitted: false,// Loader state
      status: "", // Status of the integration

      //oading
      loading: true,
      PopupLoading: false, 
      deleteLoading:false

    }

  },
  components: {
    PopUp1,
    Multiselect,
    Vue3Select,

  },
  async mounted() {
    await this.fetchTemplates()
    await this.fetchapiKey();
    await this.fetchIntegrationList();
    await this.checkIntegration();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);



    // Fetch contacts when the component is mounted
  },

  computed: {
    selectedDays() {
      return this.days.filter(day => day.selected).map(day => day.name);
    },
    isValid() {
      return this.selectedDays.length > 0; // Valid if at least one day is selected
    },
    commaSeparatedStatuses() {
      return this.selectedStatuses.map(OrderStatus => OrderStatus.value).join(",");
    },
  },

  created() {
    this.fetchProducts();
  },

  methods: {

    onTemplateSelect() {
      // Find the selected template
      const selectedTemplate = this.templates.find(template => template.id === this.selectedTemplate.id);
      console.log(this.previewData);

      // Check if the selected template has a HEADER with IMAGE format
      const headerComponent = selectedTemplate.components.find(
        component => component.type === 'HEADER' && component.format === 'IMAGE'

      );

      if (headerComponent) {
        // Show the image input field and pre-fill with the example image URL if available
        this.selectedTemplateHasImage = true;
        this.imageUrl = headerComponent.example?.header_handle?.[0] || ''; // Use the first example image if available
      } else {
        // Hide the image input field if no image is found in the template
        this.selectedTemplateHasImage = false;
        this.imageUrl = '';
      }

    },


    async disconnectWooCommerce() {
      try {
        const response = await axios.delete(`${this.apiUrl}/disconnect-woocommerce`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          }
        );
        if (response.data.status === 'success') {
          this.connectionStatus = ''; // Reset connection status
          this.store_name = '';
          this.wooAPIkey = '';
          this.wooAPIsecret = '';
          this.Base_url = '';
          this.status = 'disconnected';
          alert(response.data.message);
          // this.status="disconnected";

        } else {
          alert('Failed to disconnect from WooCommerce.');
        }
      } catch (error) {
        console.error('Error during disconnection:', error);
        alert('An error occurred while disconnecting.');
      }
    },

    async fetchProducts() {
      try {
        // Fetch product list from FastAPI
        const response = await axios.get(`${this.apiUrl}/woo_products`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          }
        );
        this.products = response.data;
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },

    saveStatuses() {
      this.commaSeparatedStatuses = this.selectedStatuses.join(",");
      // Automatically save or send the updated values to the backend
      console.log("Comma-separated values:", this.commaSeparatedStatuses);
    },

    async checkIntegration() {
      try {
        this.loading = true;
        this.error = null;

        // Call the API to check the integration
        const response = await fetch(`${this.apiUrl}/check-integration`, {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.status="disconnected"
          throw new Error(errorData.detail || "Failed to check integration.");
        }

        const data = await response.json();

        // Update the status message based on the API response
        this.statusMessage = data.message;
        this.status = data.status;
        this.store_name = data.store_info.store_name;
        this.wooAPIkey = data.store_info.consumer_key;
        this.wooAPIsecret = data.store_info.consumer_secret;
        this.Base_url = data.store_info.base_url;


      } catch (err) {
        this.error = err.message || "Something went wrong.";
      } finally {
        this.loading = false;
      }
    },

    async testWooCommerceConnection() {
      try {
        const response = await axios.post(`${this.apiUrl}/test-woocommerce`, {
          base_url: this.Base_url,
          consumer_key: this.wooAPIkey,
          consumer_secret: this.wooAPIsecret,
          store_name: this.store_name
        },
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          }
        );

        // Update UI based on the response
        this.status = "connected";
        this.checkIntegration();
        console.log("Store Info:", response.data.store_info);
      } catch (error) {
        this.connectionStatus = "Connection Failed: " + error.response.data.detail;
      }
    },



    submitIntegrationForm(action) {
      if (action == "woo/order_confirmation") {
        this.submitTemplate();
      }
      else if (action == "woo/pwn") {
        this.wooPWNform();
      }
    },

    toggleDaySelection(id) {
      const day = this.days.find(day => day.id === id);
      if (day) {
        day.selected = !day.selected;
      }
    },
    submitSelection() {
      alert(`Selected days: ${this.selectedDays.join(", ")}`);
    },

    addParameter() {
      this.parameters.push({ key: this.parameterOptions[0] }); // Add a new parameter with default value
    },

    removeParameter(index) {
      this.parameters.splice(index, 1); // Remove parameter by index
    },
    togglepopup() {
      console.log("event")
    },
    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/template`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      } catch (error) {
        console.error('Error fetching templates:', error);
      }
    },

    async fetchapiKey() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/webhooklink`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          });


        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json()
        this.webhookLink = result.webkook_link
      } catch (error) {
        console.error('Error fetching API key:', error);
      }

    },
    async submitTemplate() {
      const payload = {
        template_id: this.selectedTemplate.name,
        template_data: JSON.stringify(this.selectedTemplate),
        parameters: this.parameters,
        type: this.SelectedAction,
        product_id: this.productID,
        description:this.integration_description,
        image_id:this.media_id
      };

      // Replace with your API endpoint
      try {
        this.PopupLoading = true;
        const toast = useToast();
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/integrate/woo_order_cnf`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          toast.success("Integration saved successfully");
          this.PopupLoading = false;
          this.isSubmitted=true;
          this.fetchIntegrationList();

        } else {
          this.PopupLoading = false;
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
        // Handle successful submission
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    },
    convertISTtoUTC(timeString) {
      return new Date(new Date().toLocaleDateString("en-US", { timeZone: "Asia/Kolkata" }) + " " + timeString)
        .toISOString()
        .slice(11, 16);
    },

    async wooPWNform() {

      this.PopupLoading=true;
      this.OrderStatus = this.selectedStatuses.map(OrderStatus => OrderStatus.value).join(",");
      const payload = {
        template_id: this.selectedTemplate.name,
        template_data: JSON.stringify(this.selectedTemplate),
        parameters: this.parameters,
        type: this.SelectedAction,
        contacts_start_date: this.startDate,
        contacts_end_date: this.endDate.split("T")[0] + "T23:59:59",
        repeat_days: [...this.selectedDays],
        time: this.scheduleTime,
        rest_key: this.wooAPIkey,
        rest_secret: this.wooAPIsecret,
        product_id: this.productID,
        status: this.OrderStatus,
        base_url: this.Base_url,
        description: this.integration_description,
        image_id:this.media_id
      };
      const toast = useToast();


      if (this.isValid == false) {
        this.showError = true;
        toast.error(`Select at least one day`);
        return;
      }

      else if (this.productID == null) {
        this.showError = true;
        toast.error(`Select a product`);
        return;
      }
      else if (this.OrderStatus == null) {
        this.showError = true;
        toast.error(`Select order status`);
        return;
      }
      else if (this.startDate == null) {
        this.showError = true;
        toast.error(`Select start date`);
        return;
      }
      else if (this.endDate == null) {
        this.showError = true;
        toast.error(`Select end date`);
        return;
      }
      else if (this.scheduleTime == null) {
        this.showError = true;
        toast.error(`Select time`);
        return;
      }
      else if (this.integration_description == null) {
        this.showError = true;
        toast.error(`Enter description`);
        return;
      }


      // Replace with your API endpoint
      try {

        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/integrate/woo_pwn`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          toast.success("Integration saved successfully");
          this.PopupLoading = false;
          this.isSubmitted=true;
          this.fetchIntegrationList();

        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
        // Handle successful submission
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    },

    onFileChange(event) {
      this.file = event.target.files[0];
      this.uploadMedia();
    },


    async uploadMedia() {
      const token = localStorage.getItem('token');
      this.mediafile = event.target.files[0];
      const formData = new FormData();
      formData.append('file', this.mediafile);

      try {

        const response = await fetch(`${this.apiUrl}/upload-media`, {
          method: "POST",
          headers: {

            'Authorization': `Bearer ${token}`,
            // 'Content-Type': 'multipart/form-data',

          },
          body: formData,
        });

        const media = await response.json()
        this.media_id = media.whatsapp_media_id
        console.log(this.media_id)

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        else {
          this.uploadedMedia = true
          alert("Media Uploaded Successfully")
        }
      } catch (error) {
        console.error('Error uploading media:', error);
      }
    },


    async deleteIntegration(integration_id) {
      try {

        this.deleteLoading=true;
        const toast = useToast();
        const token = localStorage.getItem('token');
        const confirmDelete = confirm("Are you sure you want to delete this integration?                           Note:Make sure to also delete the webhook from woocommece.")
        if (!confirmDelete) return;
        const response = await fetch(`${this.apiUrl}/integration/${integration_id}`,
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );


        if (response.ok) {
          toast.success("Integration deleted successfully")
          this.fetchIntegrationList();
        }
        else {
          const errordata = await response.json()
          toast.error(`Error:${errordata.detail}`)
        }


      } catch (error) {
        console.error('Failed to delete the integration: ', error)

      }finally{
        this.deleteLoading=false;
      }
    },

    closePopup(){
      this.showPopup = false;
      this.clearForm();
    },

    clearForm() {
      this.isSubmitted=false;
      this.SelectedAction = null;
      this.selectedTemplate = null;
      this.parameters = [];
      this.productID = null;
      this.integration_description = null;
      this.scheduleTime = null;
      this.startDate = null;
      this.endDate = null;
      this.selectedStatuses = [];
    },

    async fetchIntegrationList() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/woo-integration-list`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const IntegrationList = await response.json();
        this.integrations = IntegrationList.map(integration => ({
          id: integration.id,
          description: integration.description,
          type: integration.type,
          api_key: integration.api_key,
          template: integration.template,
          integration_id: integration.integration_id
        }));
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    }
  }
}
</script>

<style scoped>
.multiselect {}

/* Add your styles here */
.woocommerceBox {
  padding: 10px;
  border-radius: 10px;
  border: solid;
  width: fit-content;
}

.webhookConfig ul li {
  margin-bottom: 5px;
}

.popup-content {
  max-height: 600px;
  /* Limit the height of the popup */
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds max-height */
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
<template>
  <div class="content-section m-8 md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold text-green-800">Broadcast Messages</h2>
        <p class="text-sm md:text-base">Send out Broadcast Messages using templates</p>
      </div>

      <div>
        <button class="bg-green-700  hover:bg-green-600  text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center "
        @click="showPopup = true, fetchContacts()">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
          </svg>
          New Broadcast
        </button>
        <!-- <button @click="showPopup = true, fetchContacts()"
          class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg ">
          
        </button> -->
      </div>
    </div>

    <PopUp v-if="showPopup" @close="closePopup()"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">


      <h2 class="text-xl font-semibold mb-4 text-green-800">New Broadcast</h2>

      <hr class="pb-4">
      

      <div class="flex">


        <div class="popup-content custom-scrollbar p-4">
          <form @submit.prevent="handleBroadcast" id="messageForm"
            :class="{ 'opacity-50 pointer-events-none': isSubmitted }"
      
            >
            

            <h4 class="text-green-700"><b>What message do you want to send?</b></h4>
            <p class="text-sm mb-2 ">Add broadcast name and template below</p>



            <div class="p-4 bg-[#f5f6fa] mb-4">

              <!-- Input Bradacast Name -->
              <div class="mb-2">
                <label for="broadcastName" class="block text-sm font-medium">Broadcast Name<span
                    class="text-red-800">*</span></label>
                <input type="text" v-model="broadcastName" id="broadcastName" placeholder="Broadcast Name" required
                  class="border border-gray-300 rounded px-3 py-2 w-full">
              </div>

              <!-- input template -->
              <div class="mb-2 ">
                <label for="templates" class="block text-sm font-medium">Choose a template<span
                    class="text-red-800">*</span></label>
                <!-- <select v-model="selectedTemplate" id="templates" required
                class="border border-gray-300 rounded px-3 py-2 w-full">
                <option value="" disabled>Select your option</option>
                <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
              </select> -->

                <!-- New select field-->
                <select id="template-select" v-model="selectedTemplateId" @change="onTemplateSelect"
                  class="border border-gray-300 rounded px-3 py-2 w-full max-h-[50px]" required>
                  <option v-for="template in templates" :key="template.id" :value="template.id">
                    {{ template.name }}
                  </option>
                </select>

                <!-- Conditional Image URL input field -->
                <div v-if="selectedTemplateHasMedia">
                  <label for="" class="block text-sm font-semibold">Upload Media</label>
                  <input type="file" @change="onFileChange" class="mb-2 w-[60%] mr-1">
                  <div v-if="uploadedMedia"><p  class="text-green-800 font-bold">Uploaded</p></div>
                  <div v-else><span class="ml-5 w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin inline-block"></span></div>
                  

                </div>
                

                <div v-if="selectedTemplateHasParameters">
                  <label for="">Select Parameter</label>
                  <select name="" id="" v-model="bodyParameter">
                    <option value="Name">Cotact_Name</option>
                  </select>
                </div>
              </div>

            </div>
            <h4 class="text-green-700"><b>Who do you want to send it to?</b></h4>
            <p class="text-sm mb-2 ">Select contacts below or <a
                href="https://drive.google.com/file/d/1hVQErwmNN6eGN1zLBoniW_34-GzAtMwm/view?usp=sharing"
                target="_blank" class="text-blue-500"><u>Download sample format for contact upload</u></a></p>

            <div class="p-4 bg-[#f5f6fa] mb-4">

              <div class="mb-2">
                <label for="recipients" class="block text-sm font-medium">Recipients<span
                    class="text-red-800">*</span></label>
                <input type="text" v-model="recipients" id="recipients"
                  placeholder="Enter phone numbers, comma-separated" required
                  class="border border-gray-300 rounded px-3 py-2 w-full">
              </div>


              <div class="mb-1">
                <label for="csvFile" class="block text-sm font-semibold">Upload CSV for Contacts:</label>
                <input type="file" @change="handleFileUpload" class="mb-2 w-[60%] mr-1" />

              </div>
            </div>
            <div v-if="csvUploaded">
              <h4><b>Imported Contacts</b></h4>
              <p class="text-sm mb-2 ">Imported contacts are not saved to your contacts directory</p>
            </div>

            <div v-else>
              <h4 class="text-green-700"><b>Contacts</b></h4>
              <p class="text-sm mb-2 ">Select from your saved contacts</p>
            </div>

            <!-- Contacts Filter -->
            <div class="flex bg-[#f5f6fa] items-center space-x-2 p-2 justify-between">
              <h3 class="text-l"><b>Filter by tags:</b></h3>

              <input type="text" v-model="tag_key" placeholder="Key"
                class="border border-gray-300 rounded px-3 py-2 w-30px">
              <input type="text" v-model="tag_value" placeholder="Value"
                class="border border-gray-300 rounded px-3 py-2 w-30px">

              <button @click.prevent="fiterBytTags"
                class=" bg-gray-300 hover:bg-gray-400 relative my-2 h-auto w-auto p-1 text-white ">Apply
                filter</button>
            </div>


            <div class="overflow-x-auto max-h-[20vh] mb-8 custom-scrollbar">
              <table class="contact-table w-full rounded-lg border-collapse">
                <thead>
                  <tr class="bg-[#ffffff] text-center">
                    <th class="z-10 p-2 bg-[#ffffff] sticky top-0">
                      <input type="checkbox" @change="selectAll($event)" v-model="allSelected"
                        class=" scale-150 m-2 z-10">Select
                    </th>
                    <th class="p-2  bg-[#ffffff] sticky top-0">Name</th>
                    <th class="p-2  bg-[#ffffff] sticky top-0">Phone Number</th>
                    <th class="p-2  bg-[#ffffff] sticky top-0">Tags</th>


                  </tr>
                </thead>
                <tbody>
                  <tr v-for="contact in contacts" :key="contact.id">
                    <td class="text-center p-2 md:p-4 scale-125">
                      <input type="checkbox" v-model="selectedContacts" :value="`${contact.name}:${contact.phone}`">
                    </td>

                    <td class="text-center p-2 md:p-4">{{ contact.name }}</td>
                    <td class="text-center p-2 md:p-4">{{ contact.phone }}</td>
                    <td class="text-center p-2 md:p-4">
                      <div v-for="(tag, index) in contact.tags" :key="index">
                        <span class="font-bold">{{ tag.key }}:</span> {{ tag.value }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>


            <h4 class="text-green-700"><b>When do you want to send the message ?</b></h4>
            <p class="text-sm mb-2 ">Select from the options below </p>


            <div class="p-4 bg-[#f5f6fa] mb-4">


              <p class=" text-sm font-semibold mb-1"><input type="radio" v-model="isScheduled" :value="false"
                  class="scale-150 text-green-500 m-2 accent-green-700">Send Now</p>

              <p class="text-sm font-semibold mb-1"><input type="radio" v-model="isScheduled" :value="true"
                  class="scale-150 text-green-500 m-2 accent-green-700" @click="currentDateTime">Schedule </p>

              <div v-if="isScheduled" class="flex justify-between">
                <div class="w-[50%]">
                  <label for="scheduleDate" class="block text-sm font-medium">Date<span
                      class="text-red-800">*</span></label>
                  <input type="date" v-model="scheduleDate" id="scheduleDate" required
                    class="border border-gray-300 rounded px-3 py-2 w-full">
                </div>
                <div class="w-[50%]">
                  <label for="scheduleTime" class="block text-sm font-medium">Time<span
                      class="text-red-800">*</span>(GMT
                    +5:30)</label>
                  <input type="time" v-model="scheduleTime" id="scheduleTime" required
                    class="border border-gray-300 rounded px-3 py-2 w-full">
                </div>
              </div>
            </div>
            <!-- <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">{{ isScheduled ?
              'Schedule Message' : 'Send Message' }}</button> -->

              <button
              type="submit"
              class="bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center "
              :disabled="popupLoading || isSubmitted">
              <span v-if="popupLoading"
                class="animate-spin border-2 border-white border-t-transparent rounded-full w-4 h-4 mr-2"></span>
              {{ isSubmitted ? "Submitted" : popupLoading ? "Submitting..." : isScheduled ?
                'Schedule Message' : 'Send Message' }}
            </button>
          </form>
        </div>


        <!-- Template preview  -->

        <!-- <div class="flex justify-center items-center h-screen bg-gray-200">
          <div class="w-80 h-[550px] bg-white rounded-3xl shadow-lg border-4 border-black flex flex-col">
            <div class="h-12 bg-black rounded-t-3xl flex items-center justify-center text-white font-semibold">
              Phone Screen
            </div>
            <div class="flex-1 overflow-y-auto p-4">
              <div
          class="flex flex-col aspect-[10/19] min-w-[320px] p-3 max-h-[670px] bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center custom-scrollbar">
          <div class="message">
            <span style="white-space: pre-line;" v-html="previewData"></span>
          </div>
        </div>
            </div>
          </div>
        </div> -->

        <div
          class="flex flex-col flex-grow h-full overflow-y-auto aspect-[10/19] min-w-[320px] p-3 max-h-[600px]  bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center custom-scrollbar">
          <div class="message">
            <span style="white-space: pre-line;" v-html="previewData"></span>
          </div>
        </div>

      </div>


    </PopUp>


    <div class="p-4  filter-container space-x-2">

      <div class="flex items-center">
        <h3 class="text-xl md:text-2xs mb-2 text-green-700"><b>Broadcast List </b></h3>
        <div class="pb-2 pl-2">
          <button class=" text-green-600 underline hover:text-green-700 hover:bg-transparent"
            @click="fetchBroadcastList(this.filterStatus, 1)">
             <i class="bi bi-arrow-clockwise inline-block text-xl" :class="{ 'animate-spin': loading }"></i> 
          </button>
        </div>

      </div>

      <div class="flex justify-between">
        <div class="flex items-center filter-container space-x-2">
          <h3><b>Filter by:</b></h3>
          <div class="w-40px">
            <select name="" id="" @change="filterBroadcastsByStatus" class="border border-gray-300 rounded px-3 py-2 ">
              <option value="null">Status</option>
              <option value="Successful">Successful</option>
              <option value="Cancelled">Cancelled</option>
              <option value="Partially Successful">Partially Successful</option>
            </select>
          </div>
        </div>

      </div>
    </div>

    <div class="overflow-x-auto max-h-[51vh] custom-scrollbar">
      <table class="w-full border border-gray-300 rounded-lg text-sm md:text-base bg-white">
        <thead>
          <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
            <th class="p-3 md:p-4 text-left border border-gray-300 sticky top-0 z-10 bg-gray-100">Broadcast Name</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Type</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Template</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Contacts</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Status</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="broadcast in broadcasts" :key="broadcast.id" class="hover:bg-gray-50">
            <td class="p-3 md:p-4 text-left border border-gray-200">{{ broadcast.name }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ broadcast.type }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ broadcast.template }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ broadcast.contacts.length }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <div :class="{
                  'text-emerald-600 font-semibold': broadcast.status === 'Successful',           // Green: Success
                  'text-sky-600 font-semibold': broadcast.status === 'Scheduled',                // Blue: Info/Scheduled
                  'text-rose-600 font-semibold': broadcast.status === 'Cancelled',              // Red: Danger/Cancelled
                  'text-amber-600 font-semibold': broadcast.status === 'Partially Successful',  // Amber: Warning/Partial
                  'text-indigo-600 font-semibold': broadcast.status === 'processing...', 
              }">
                {{ broadcast.status }}
              </div>
            </td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <button class="underline text-gray-800 hover:bg-inherit font-medium"
                @click="showReportPopup = true, fetchBroadcastReport(broadcast.id)">
                View Report
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>



    
    <div class="flex justify-center mt-4">
      <div class="flex items-center space-x-4 bg-white shadow-md rounded-lg px-4 py-2">
        <button
          class="px-3 py-1 bg-green-500 text-white font-medium rounded hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="loadPreviousPage"
          :disabled="currentPage === 1"
        >
          Previous
        </button>
        <div class="px-4 py-1 border border-gray-300 rounded text-gray-700 font-semibold">
          {{ currentPage }}
        </div>
        <button
          class="px-3 py-1 bg-green-500 text-white font-medium rounded hover:bg-green-600"
          @click="loadNextPage"
        >
          Next
        </button>
      </div>
    </div>




    <PopUp1 v-if="showReportPopup" @close="showReportPopup = false, broadcastReports = ['']">

      <h3 class="text-xl md:text-2xs mb-4"><b>Broadcast Report</b></h3>

      <!-- show the overview totals -->

      <div class="grid grid-cols-4 gap-4 p-4">
        <!-- Sent -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">

          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.sent }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="18"
                height="14" viewBox="0 0 18 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1.66797 7L7.16797 12.5L16.3346 1.5" stroke="#23A455" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round"></path>
              </svg></div>
          </div>


          <span class="text-gray-500">Sent</span>
        </div>

        <!-- Delivered -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">

          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.delivered }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="22"
                height="12" viewBox="0 0 22 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1.83203 6L6.64453 10.5833L9.05078 7.83333" stroke="#23A455" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"></path>
                <path d="M7.33203 5.99984L12.1445 10.5832L20.1654 1.4165" stroke="#23A455" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"></path>
                <path d="M14.6654 1.4165L11.457 5.08317" stroke="#23A455" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round"></path>
              </svg></div>
          </div>


          <span class="text-gray-500">Delivered</span>
        </div>

        <!-- Read -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.read }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="22"
                height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M20.2565 6.962C20.7305 7.582 20.7305 8.419 20.2565 9.038C18.7635 10.987 15.1815 15 10.9995 15C6.81752 15 3.23552 10.987 1.74252 9.038C1.51191 8.74113 1.38672 8.37592 1.38672 8C1.38672 7.62408 1.51191 7.25887 1.74252 6.962C3.23552 5.013 6.81752 1 10.9995 1C15.1815 1 18.7635 5.013 20.2565 6.962V6.962Z"
                  stroke="#23A455" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                <path
                  d="M11 11C12.6569 11 14 9.65685 14 8C14 6.34315 12.6569 5 11 5C9.34315 5 8 6.34315 8 8C8 9.65685 9.34315 11 11 11Z"
                  stroke="#23A455" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
              </svg></div>

          </div>
          <span class="text-gray-500">Read</span>
        </div>

        <!-- Replied -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.replied }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Replied</span>
        </div>

        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.sent }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Success</span>
        </div>

        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.failed }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Failed</span>
        </div>
      </div>


    <div class="p-4 overflow-x-auto max-h-[51vh] custom-scrollbar">
      <table class="w-full border border-gray-300 rounded-lg text-sm md:text-base bg-white">
        <thead>
          <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Name</th>
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Phone No</th>
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Status</th>
              <!-- <th class="p-2 md:p-4 border-b-2 sticky top-0">Sent</th>
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Delivered</th>
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Read</th>
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Replied</th> -->
              <th class="p-2 md:p-4 border-b-2 sticky top-0">Failure Reason</th>

            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="(contactReport, index) in broadcastReports" :key="contactReport.id">
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.contact_name }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.phone_no }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.status }}</td>
              <!-- <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.sent }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.delivered }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.read }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.replied }}</td> -->
              <td class="border-[#ddd] p-2 md:p-4 text-center">
                <div class="relative flex justify-center items-center">
                  <button v-if="contactReport.error_reason" @mouseenter="showTooltip(index, $event)"
                    @mouseleave="hideTooltip" class="info-button">
                    ℹ️
                  </button>
                  <div v-if="tooltipVisible === index"
                    class="tooltip-container absolute bg-gray-700 text-white p-2 rounded text-sm"
                    :style="tooltipStyles">
                    {{ contactReport.error_reason }}
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>




    </PopUp1>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp1 from "../popups/popup1";
import PopUp from "../popups/popup";
import axios from "axios";
export default {
  name: 'BroadCast2',

  components: {
    PopUp,
    PopUp1
  }
  ,
  props: {
    contactReport: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {

      apiUrl: process.env.VUE_APP_API_URL,

      // Tmeplate preview
      previewData: null,

      loading: false,
      currentPage: 1,
      tooltipVisible: null, // Index of the row with a visible tooltip
      tooltipStyles: {},
      mediafile: null,
      mediaId: "",
      uploadedMedia: false,

      broadcastName: '',
      recipients: '',
      selectedTemplate: '',
      templates: [],
      contacts: [],
      broadcasts: [],
      // broadcast report
      broadcastReports: [],
      totalRead: '',
      totalSent: '',
      totalDelivered: '',
      csvUploaded: false,

      allSelected: false,


      csvFile: null,
      selectedContacts: [],
      showPopup: false,
      showReportPopup: false,
      scheduleDate: '',  // New data property for schedule date
      scheduleTime: '',
      isScheduled: false,


      selectedTemplateId: null, // Holds the selected template's ID
      selectedTemplateHasMedia: false, // Boolean to control if image URL input should appear
      imageUrl: '',// To store the input value for the image URL
      selectedTemplateHasParameters: false,
      bodyParameters: [],
      bodyParameter: '',


      filterStatus: null,

      // loading
      popupLoading: false,
      isSubmitted: false,
      tableLoading: false

    };
  },
  async mounted() {
    // await this.fetchTemplates();
    await this.fetchContacts();
    await this.fetchBroadcastList();
    await this.fetchtemplateList();



    // Fetch contacts when the component is mounted
  },
  methods: {


    generateTemplatePreview(components) {
      let previewMessage = '';


      // Loop through components and construct the preview message
      components.forEach(component => {
        switch (component.type) {
          case 'HEADER': {
            if (component.format === 'TEXT') {
              previewMessage += `<strong>${component.text}\n</strong> `;
            } else if (component.format === 'IMAGE' && component.example?.header_handle) {
              previewMessage += `<div style="width: auto; height: 200px; overflow: hidden; position: relative; border-radius: 5px">
  <img src="${component.example.header_handle[0]}" alt="Description of image" 
       style="width: 100%; height: 100%; object-fit: cover; object-position: start; display: block ; border-radius: 4px">
</div>`;

            }
            else if (component.format === 'VIDEO' && component.example?.header_handle) {
              previewMessage += `<div style="width: auto; height: 200px; overflow: hidden; position: relative; border-radius: 5px">
                <video controls 
                    src="${component.example.header_handle[0]}" 
                    style="width: 100%; height: 100%; object-fit: cover; object-position: start; display: block; border-radius: 4px">
                    Your browser does not support the video tag.
                </video>
            </div>`;
            }
            break;
          }
          case 'BODY': {
            let bodyText = component.text;
            // Check if the body contains dynamic placeholders like {{1}}
            bodyText = this.replacePlaceholders(bodyText, component.example?.body_text);
            previewMessage += bodyText;

            break;
          }
          case 'FOOTER': {
            previewMessage += `<span style="font-weight: lighter; color:gray;">\n${component.text}</span> `;
            break;
          }
          case 'BUTTONS': {
            if (component.buttons && Array.isArray(component.buttons)) {
              previewMessage += `<div style=" text-align: left;">`;
              component.buttons.forEach(button => {
                if (button.type === 'URL') {
                  previewMessage += `
          <a href="${button.url}" target="_blank" 
             style="display: inline-flex; align-items: center; 
                    text-decoration: none; font-weight: bold; color: #007bff; 
                     border-top: 1px solid #ddd;">
            <svg xmlns="http://www.w3.org/2000/svg" fill="#007bff" width="19" height="19" viewBox="0 0 24 24" style="margin-right: 5px;">
              <path d="M14 3v2h3.586l-8.293 8.293 1.414 1.414 8.293-8.293v3.586h2v-7h-7z"/>
              <path d="M5 5h6v-2h-6c-1.103 0-2 .897-2 2v14c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-6h-2v6h-14v-14z"/>
            </svg>
            <span style="padding:5px">${button.text}</span>
            
          </a>`;
                } else if (button.type === 'REPLY') {
                  previewMessage += `
          <button style="display: inline-block; margin: 5px 0; padding: 10px 15px; 
                         background-color: #007bff; color: white; border: none; 
                         border-radius: 20px; cursor: pointer; font-weight: bold;">
            ${button.text}
          </button>`;
                }
              });
              previewMessage += `</div>`;
            }
            break;
          }

          default: {
            previewMessage += `[Unknown Component Type] `;
            break;
          }
        }
      });

      return previewMessage;
    },

    // Replace placeholders with example data (or default values if not available)
    replacePlaceholders(bodyText, example) {
      if (example && example.length > 0) {
        // Assuming example contains placeholder names like "Name"
        example.forEach((param, index) => {
          const placeholder = `${index + 1}`;
          bodyText = bodyText.replace(placeholder, param[0]); // Replace with the actual placeholder value
        });
      }
      // console.log(bodyText);
      return bodyText;
    },


    async loadNextPage() {
      const prevFirst = this.broadcasts[0]?.id;
      await this.fetchBroadcastList(this.filterStatus, this.currentPage+1);
      const newFirst = this.broadcasts[0]?.id;

      if (prevFirst !== newFirst && this.broadcasts.length > 0) {
        this.currentPage += 1;
      }
    },
    async loadPreviousPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        await this.fetchBroadcastList(this.filterStatus, this.currentPage);
      }
    },

    showTooltip(index, event) {
      this.tooltipVisible = index; // Set the visible tooltip to the current row index
      const { clientX: x, clientY: y } = event;
      this.tooltipStyles = {
        left: `${x}px`,
        top: `${y + 15}px`, // Offset for better visibility
      };
    },
    hideTooltip() {
      this.tooltipVisible = null; // Hide the tooltip
    },

    // showTooltip(event) {
    //   this.tooltipVisible = true;
    //   const buttonRect = event.target.getBoundingClientRect();
    //   this.tooltipStyles = {
    //     top: `${buttonRect.bottom + 8}px`, // Position below the button with a small gap
    //     left: `${buttonRect.left + buttonRect.width / 2 - 85}px`, // Center horizontally, adjust for half of 170px width
    //     width: "170px", // Tooltip width
    //     height: "100px", // Tooltip height
    //   };
    // },

    // hideTooltip() {
    //   this.tooltipVisible = false;
    // },




    async fetchtemplateList() {
      const token = localStorage.getItem('token');

      try {
        const response = await fetch(`${this.apiUrl}/template`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
      }
    },

    async onTemplateSelect() {
      // Find the selected template
  
      const selectedTemplate = this.templates.find(template => template.id === this.selectedTemplateId);
      this.previewData = this.generateTemplatePreview(selectedTemplate.components);
      console.log(this.previewData);

      // Check if the selected template has a HEADER with IMAGE format
      const headerComponent = selectedTemplate.components.find(
        component => component.type === 'HEADER' && (component.format === 'IMAGE' || component.format === 'VIDEO')

      );

      // if (headerComponent) {
      //   // Show the image input field and pre-fill with the example image URL if available
      //   this.selectedTemplateHasMedia = true;
      //   this.imageUrl = headerComponent.example?.header_handle?.[0] || ''; // Use the first example image if available
      // } else {
      //   // Hide the image input field if no image is found in the template
      //   this.selectedTemplateHasMedia = false;
      //   this.imageUrl = '';
      // }

      if (headerComponent) {
        this.selectedTemplateHasMedia = true;
        this.imageUrl = headerComponent.example?.header_handle?.[0] || '';

        if (this.imageUrl) {
          try {
            const token = localStorage.getItem('token'); // or however you're storing it
            const downloadUrl = new URL("http://localhost:8000/download-media");
            downloadUrl.searchParams.append("media_url", this.imageUrl);

            const response = await fetch(downloadUrl.toString(), {
              headers: {
                Authorization: `Bearer ${token}`
              }
            });

            if (!response.ok) {
              throw new Error(`Download failed with status ${response.status}`);
            }

            const blob = await response.blob();
            console.log("Blob received:", blob);
            const contentType = response.headers.get("content-type") || "application/octet-stream";
            const ext = contentType.split("/")[1] || "bin";
            const file = new File([blob], `template-media.${ext}`, { type: contentType });

            const fakeEvent = {
              target: {
                files: [file]
              }
            };

            await this.onFileChange(fakeEvent);
            this.popupLoading = false;
            console.log(`Template media downloaded and uploaded successfully.: ${this.mediaId}`);
          } catch (error) {
            console.error("Failed to download/upload template media:", error);
          }
        }
      } else {
        this.selectedTemplateHasMedia = false;
        this.imageUrl = '';
      }




      // Check if the selected template has BODY parameters
      const bodyComponent = selectedTemplate.components.find(component => component.type === 'BODY');

      if (bodyComponent && bodyComponent.text.includes('{{')) {
        // Extract the parameters from the body text if there are placeholders
        const parameterMatches = bodyComponent.text.match(/{{\d+}}/g);
        if (parameterMatches) {
          this.selectedTemplateHasParameters = true;
          this.bodyParameters = parameterMatches.map((param, index) => ({
            name: `Parameter ${index + 1}`,
            value: ''
          }));
        } else {
          this.selectedTemplateHasParameters = false;
          this.bodyParameters = [];
        }
      } else {
        // Hide the parameter input fields if no parameters are found
        this.selectedTemplateHasParameters = false;
        this.bodyParameters = [];
      }
    },



    async fetchContacts() {

      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.apiUrl}/contacts/?limit=1000&offset=0`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const contactList = await response.json();
        this.contacts = contactList.map(contact => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },

    async fetchBroadcastList(statusFilter = null, page = 1) {
      const token = localStorage.getItem('token'); // Retrieve token from localStorage
      const itemsPerPage = 10;

      this.filterStatus = statusFilter;// Number of items to display per page
      const url = `${this.apiUrl}/broadcast?limit=${itemsPerPage}&offset=${(page - 1) * itemsPerPage}&statusfilter=${this.filterStatus}`;

      try {
        // Fetch data from the backend
        this.loading = true;
        // await new Promise(resolve => setTimeout(resolve, 2000));
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        // Check if the response is OK
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        // Parse JSON response
        const broadcastList = await response.json();
        this.loading = false;
        // Process and optionally filter broadcasts
        this.broadcasts = broadcastList
          .map((broadcast) => ({
            id: broadcast.id,
            name: broadcast.name,
            type: broadcast.type,
            template: broadcast.template,
            contacts: broadcast.contacts,
            success: broadcast.success,
            failed: broadcast.failed,
            status: broadcast.status,
            created_at: broadcast.created_at, // Include for sorting
            updated_at: broadcast.updated_at, // Include for sorting
          }))
        // .filter((broadcast) => {
        //   return statusFilter ? broadcast.status === statusFilter : true;
        // }); 

        console.log('Broadcasts:', this.broadcasts); // Debug: Log the fetched broadcasts
      } catch (error) {
        console.error('Error fetching broadcasts:', error); // Log errors
      }
    },




    filterBroadcastsByStatus(event) {
      const status = event.target.value;
      this.fetchBroadcastList(status);
    },

    formatDateTime(date) {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    },

    updateRecipients() {
      this.recipients = this.selectedContacts.join(', ');
    },


    async onFileChange(event) {
      this.mediafile = event.target.files[0];
      this.uploadMedia();
    },


    async uploadMedia() {
      if (!this.mediafile) {
        console.error("No file available for upload");
        return;
      }
      const token = localStorage.getItem('token');

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
        this.mediaId = media.whatsapp_media_id
        console.log(this.mediaId)

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        else {
          this.uploadedMedia = true
          // alert("Media Uploaded Successfully")
        }
      } catch (error) {
        console.error('Error uploading media:', error);
      }
    },



    async sendBroadcast() {
      const toast = useToast();


      // Assuming recipients have both name and number in format 'Name:1234567890'
      const contacts = this.recipients.split(',').map(entry => {
        const [name, phone] = entry.split(':').map(item => item.trim());
        return { name, phone };
      });

      const Template = this.templates.find(template => template.id === this.selectedTemplateId);
      const selectedTemplate = Template.name;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;

      const mediaID = this.mediaId;
      const token = localStorage.getItem('token');
      const bodyparamter = this.bodyParameter

      try {
        this.popupLoading = true;
        this.fetchBroadcastList();

        const requestBody = {
          name: broadcastNameWithDate,
          recipients: contacts, // Now sending both name and number
          template: selectedTemplate,
          template_data: JSON.stringify(Template),
          type: "Broadcast",
          status: 'Saved',
        };

        if (mediaID) {
          requestBody.image_id = mediaID;
        }

        if (bodyparamter) {
          requestBody.body_parameters = bodyparamter;
        }

        const response = await fetch(`${this.apiUrl}/send-template-message/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        } else {
          this.fetchBroadcastList();
          this.popupLoading = false;
          this.isSubmitted = true;
          toast.success('Broadcast sent successfully');
        }



      } catch (error) {
        console.error('Error sending broadcast:', error);

      }
    },


    closePopup() {
      this.showPopup = false;
      this.clearForm();
    },

    async fetchBroadcastReport(broadcast_id) {


      const token = localStorage.getItem('token');
      try {

        const response = await fetch(`${this.apiUrl}/broadcast-report/${broadcast_id}`, {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json()
        this.broadcastReports = result.map(report => ({

          phone_no: report.phone_no,
          contact_name: report.contact_name,
          status: report.status,
          sent: report.sent,
          delivered: report.delivered,
          read: report.read,
          replied: report.replied,
          error_reason: report.error_reason

        }));

      } catch (error) {
        console.error("Error fetching report for the broadcast", error)
      }
    },

    handleBroadcast() {
      if (this.isScheduled) {
        this.scheduleBroadcast2();

      } else {
        this.sendBroadcast();
      }
    },
    async scheduleBroadcast2() {

      const contacts = this.recipients.split(',').map(entry => {
        const [name, phone] = entry.split(':').map(item => item.trim());
        return { name, phone };
      });


      // Logic for scheduling a broadcast
      const toast = useToast();
      // const phoneNumbers = this.recipients.split(',').map(num => num.trim());
      const Template = this.templates.find(template => template.id === this.selectedTemplateId);
      const selectedTemplate = Template.name;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      // responseDiv.textContent = 'Scheduling...';
      const token = localStorage.getItem('token');
      const mediaID = this.mediaId;
      const bodyparamter = this.bodyParameter

      // Combine date and time for scheduling
      const scheduledDatetime = new Date(`${this.scheduleDate}T${this.scheduleTime}`).toISOString();

      try {
        this.popupLoading = true;
        this.fetchBroadcastList();




        const requestBody = {
          name: broadcastNameWithDate,
          recipients: contacts,
          template: selectedTemplate,
          template_data: JSON.stringify(Template),
          type: "Scheduled",
          status: 'Saved',
          scheduled_time: scheduledDatetime
        };

        if (mediaID) {
          requestBody.image_id = mediaID;
        }

        if (bodyparamter) {

          requestBody.body_parameters = bodyparamter;
        }

        const response = await fetch(`${this.apiUrl}/schedule-template-message/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errorData = await response.json(); // Parse the response JSON
          const errorMessage = errorData.detail || 'Unknown error'; // Extract error message
          toast.error(`Error scheduling broadcast: ${errorMessage}`);
          // alert(`Error scheduling broadcast: ${errorMessage}`);
          throw new Error('Network response was not ok');
        } else {
          toast.success('Broadcast scheduled successfully!');
          this.popupLoading = false;
          this.isSubmitted = true;
          this.fetchBroadcastList();
        }

      } catch (error) {
        console.error('Error scheduling broadcast:', error);
        responseDiv.textContent = 'Error scheduling broadcast.';
      }
    },


    clearForm() {
      this.popupLoading = false;
      this.isSubmitted = false,
        this.contact = "",
        this.previewData = '';
      this.broadcastName = '',
        this.selectedTemplateHasParameters = '',
        this.selectedTemplateHasMedia = false,
        this.selectedTemplateId = '',
        this.bodyParameter = '',
        this.recipients = '',
        this.selectedTemplate = '',
        this.csvFile = null,
        this.mediaId = "",
        this.mediafile = null,
        this.uploadedMedia = false,
        this.selectedContacts = [],
        this.scheduleDate = '',  // New data property for schedule date
        this.scheduleTime = '',
        this.isScheduled = false,
        this.contacts = [],
        this.csvUploaded = false

    },

    handleFileUpload(event) {
      this.csvFile = event.target.files[0];
      this.importCSV();

    },


    async importCSV() {
      const toast = useToast();
      if (!this.csvFile) return;

      const formData = new FormData();
      const token = localStorage.getItem("token");
      formData.append("file", this.csvFile);

      try {
        const response = await axios.post(`${this.apiUrl}/contacts/bulk_import/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        });

        // Handle the response directly
        if (response.status >= 200 && response.status < 300) {
          toast.success("Contact created successfully");

          const { contacts, duplicates } = response.data; // Extract contacts and duplicates
          this.contacts = [...contacts, ...duplicates]; // Merge contacts and duplicates
          this.csvUploaded = true;

          // Format and append contacts in the required format 'Name:1234567890'
          const formattedContacts = this.contacts
            .map((contact) => `${contact.name}:${contact.phone}`)
            .join(',');

          // Update recipients with formatted contact list
          this.recipients = this.recipients
            ? `${this.recipients},${formattedContacts}`
            : formattedContacts;
        } else {
          toast.error(`Error: ${response.data?.detail || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error importing contacts:", error.response?.data?.detail || error.message);
        toast.error(`Error: ${error.response?.data?.detail || "Something went wrong"}`);
      }
    },


    async fiterBytTags() {
      const token = localStorage.getItem("token");
      const tagValue = this.tag_value
      const tagKey = this.tag_key
      try {

        const response = await fetch(`${this.apiUrl}/contacts-filter/filter?tag_key=${tagKey}&tag_value=${tagValue}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });


        const contactsList = await response.json()
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
          created_at: contact.created_at, // Store raw dates for sorting
          updated_at: contact.updated_at // Store updated_at too
        }));

        if (!response.ok) {
          throw new Error("Network response not ok")
        }

      } catch (error) {
        console.error("Error filtering contacts", error)
      }
    },

    selectAll(event) {
      // Check if the "Select All" checkbox is checked or unchecked
      if (event.target.checked) {
        // Select all contacts by pushing all contact phone numbers to the selectedContacts array
        this.selectedContacts = this.contacts.map(contact => `${contact.name}:${contact.phone}`);
      } else {
        // Deselect all contacts by clearing the selectedContacts array
        this.selectedContacts = [];
      }
    },

    currentDateTime() {
      const now = new Date();

      // Format the date as YYYY-MM-DD
      const year = now.getFullYear();
      const month = (now.getMonth() + 1).toString().padStart(2, '0');
      const day = now.getDate().toString().padStart(2, '0');
      this.scheduleDate = `${year}-${month}-${day}`;

      // Add 5 minutes to the current time
      now.setMinutes(now.getMinutes() + 2);
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      this.scheduleTime = `${hours}:${minutes}`;
    },

    async ImportCSV() {
      const toast = useToast();
      if (!this.file) return;

      const formData = new FormData();
      const token = localStorage.getItem("token");
      formData.append("file", this.file);

      try {
        const response = await axios.post(`${this.apiUrl}/contacts/bulk_import/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        });

        // Handle the response directly
        if (response.status >= 200 && response.status < 300) {
          toast.success("Contact created successfully");


          // Format and append contacts in the required format 'Name:1234567890'
          const formattedContacts = this.contacts.map(contact => `${contact.name}:${contact.phone}`).join(',');

          // Update recipients with formatted contact list
          this.recipients = this.recipients ? `${this.recipients},${formattedContacts}` : formattedContacts;

        } else {
          toast.error(`Error: ${response.data?.detail || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error importing contacts:", error.response?.data?.detail || error.message);
        toast.error(`Error: ${error.response?.data?.detail || "Something went wrong"}`);
      }
    },


  },
  computed: {
    totals() {
      return this.broadcastReports.reduce(
        (acc, report) => {
          acc.sent += report.sent ? 1 : 0;
          acc.delivered += report.delivered ? 1 : 0;
          acc.read += report.read ? 1 : 0;
          acc.replied += report.replied ? 1 : 0;
          acc.failed += report.status === "failed" ? 1 : 0;
          return acc;
        },
        { sent: 0, delivered: 0, read: 0, replied: 0, failed: 0 } // Initial count set to 0 for all
      );
    }
  },
  watch: {
    selectedContacts: function () {
      this.updateRecipients();
    },
    selectedContactsAll(newSelectedContacts) {
      // Check if all contacts are selected
      this.updateRecipients();
      this.allSelected = newSelectedContacts.length === this.contacts.length;
    },
    mounted() {
      // Get the current date and time

    }
  }
};
</script>

<style scoped>


.tooltip-container {
  display: flex;
  position: fixed;
  /* Ensure the tooltip floats independently */
  align-items: center;
  /* Vertically center content */
  justify-content: center;
  /* Horizontally center content */
  width: 170px;
  /* Fixed width */
  height: 100px;
  /* Fixed height */
  background-color: #444;
  /* Background color for visibility */
  color: white;
  /* Text color */
  border-radius: 8px;
  /* Rounded corners */
  z-index: 100000;
  /* Ensure it's above other elements */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  /* Add shadow */
  padding: 8px;
  /* Inner spacing */
  text-align: center;
  /* Center text alignment */
  overflow: hidden;
  /* Prevent text from spilling out */
  word-wrap: break-word;
  /* Ensure long words break */
  white-space: normal;
  /* Wrap text onto the next line */
  line-height: 1.2;
  /* Adjust line spacing for readability */
  box-sizing: border-box;
  /* Include padding in dimensions */
}



.info-button {
  display: inline-flex;       /* Use inline-flex so it wraps to content */
  align-items: center;
  cursor: pointer;
  color: blue;
  padding: 4px 8px;           /* Small padding around the text */
  border: 1px solid blue;     /* Optional: add a border */
  border-radius: 4px;         /* Slightly rounded corners */
  font-size: 14px;            /* Optional: control font size */
  background-color: #f0f8ff;  /* Optional: light background */
  width: fit-content;         /* Ensure it fits content size */
}

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

.my-custom-toast {
  background-color: #4caf50;
  /* Custom background */
  color: white;
  font-size: 16px;
  border-radius: 10px;
}

.popup-content {
  max-height: 600px;
  /* Limit the height of the popup */
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds max-height */
}

.message {
  font-size: small;
  display: flex;
  justify-content: space-between;
  background-color: #ffffff;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  max-width: 90%;
  min-width: 80px;
  height: auto;
  max-height: 650px;
  word-wrap: break-word;
  word-break: break-word;
  width: fit-content;
  overflow: hidden;

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

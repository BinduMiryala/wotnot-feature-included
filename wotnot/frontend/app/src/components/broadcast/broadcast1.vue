<template>
  <div class="content-section m-8 md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Manage Templates</h2>

        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>

      <div>
        <!-- <button @click="showPopup = true"
          class="text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base w-full md:w-auto">
          Create New Template
        </button> -->
        <button
          class="bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478] transition-all duration-300"
          @click="showPopup = true">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
          </svg>
          New Template
        </button>

      </div>
    </div>

    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Template List</b><span v-if="cursor"
        class="ml-5 w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin inline-block"></span>
    </h3>


    <div class="overflow-x-auto max-h-[55vh] custom-scrollbar mb-2">
      <table class="w-full border border-gray-300 rounded-lg text-sm md:text-base bg-white"
        :class="{ 'opacity-50 pointer-events-none': tableLoading }">
        <thead>
          <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
            <th class="p-3 md:p-4 text-left border border-gray-300 sticky top-0 z-10 bg-gray-100">Name</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Language</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Status</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Category</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Sub Category</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">ID</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Preview</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Actions</th>
          </tr>
        </thead>
        <tbody class="">
          <tr v-for="template in templates" :key="template.id" class="hover:bg-gray-50">
            <td class="p-3 md:p-4 text-left border border-gray-200">{{ template.name }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ template.language }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <div :class="{
                ' text-green-600 font-semibold px-2 py-1 rounded': template.status === 'APPROVED',
                ' text-blue-600 font-semibold px-2 py-1 rounded': template.status === 'PENDING',
                ' text-red-500 font-semibold px-2 py-1 rounded': template.status === 'REJECTED'
              }">
                {{ template.status }}
              </div>
            </td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ template.category }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ template.sub_category }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ template.id }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <button class="text-gray-600 underline hover:text-gray-800 hover:bg-inherit font-medium"
                @click="showpreview(template.preview)">
                Preview
              </button>
            </td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <button @click="showConfirmationPopup(template.name)" class="hover:bg-white rounded-full p-2 transition">
                <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                  colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                </lord-icon>
              </button>
            </td>
            
              
            
           
          </tr>
        </tbody>
      </table>
    </div>



    <confirmationPopup  v-if="showConfirmPopup" @yes="deleteTemplate(deleteTemplateName)" @no="showConfirmPopup = false" @close="showConfirmPopup = false" />

    <PopUp_preview v-if="showPreview" @close="closePreview">

      <div
        class="flex flex-col aspect-[10/19] p-3 max-h-[670px] bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center custom-scrollbar">
        <div class="message">
          <span style="white-space: pre-line;" v-html="preview_data"></span>
        </div>
      </div>

    </PopUp_preview>

    <PopUp v-if="showPopup" @close="closePopup"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">


      <h2 class="text-xl font-semibold mb-4 text-green-800">Create Message Template</h2>

      <hr class="pb-4">


      <div>

        <div class="flex ">
          <div class="mr-4 max-h-[600px] overflow-y-auto custom-scrollbar">
            <form class="p-4" :class="{ 'opacity-50 pointer-events-none': isSubmitted }">
              <h4 class="text-green-800"><b>Template name and language</b></h4>
              <p class="text-sm mb-2 ">Categorize your template</p>
              <div class="grid grid-cols-3 gap-4 bg-[#f5f6fa] p-4 mb-2">
                <div>
                  <label class="block below-402:text-custom-small text-sm font-medium">Template Name
                    <span class="text-red-800">*</span>
                  </label>
                  <div class="relative mb-2">
                    <input v-model="template.name" :placeholder="'Template Name'"
                      @blur="validateTemplateName" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10" required />
                                    <span v-if="nameError" class="text-red-500 text-xs absolute top-full left-0 mt-1">
                      {{ nameError }}</span>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium">Category<span class="text-red-800">*</span></label>
                  <select v-model="selectedCategory" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10"
                    required>
                    <option value="Marketing">Marketing</option>
                    <option value="Utility">Utility</option>
                  </select>
                </div>

                <!-- Language -->
                <div class="mb-4">
                  <label class="block text-sm font-medium">Language<span class="text-red-800">*</span></label>
                  <select v-model="selectedLanguage" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10"
                    required>
                    <option value="af">Afrikaans</option>
                    <option value="sq">Albanian</option>
                    <option value="ar">Arabic</option>
                    <option value="az">Azerbaijani</option>
                    <option value="bn">Bengali</option>
                    <option value="bg">Bulgarian</option>
                    <option value="ca">Catalan</option>
                    <option value="zh_CN">Chinese (Simplified)</option>
                    <option value="zh_HK">Chinese (Hong Kong)</option>
                    <option value="zh_TW">Chinese (Taiwan)</option>
                    <option value="hr">Croatian</option>
                    <option value="cs">Czech</option>
                    <option value="da">Danish</option>
                    <option value="nl">Dutch</option>
                    <option value="en">English</option>
                    <option value="en_GB">English (UK)</option>
                    <option value="en_US" default>English (US)</option>
                    <option value="et">Estonian</option>
                    <option value="fil">Filipino</option>
                    <option value="fi">Finnish</option>
                    <option value="fr">French</option>
                    <option value="ka">Georgian</option>
                    <option value="de">German</option>
                    <option value="el">Greek</option>
                    <option value="gu">Gujarati</option>
                    <option value="ha">Hausa</option>
                    <option value="he">Hebrew</option>
                    <option value="hi">Hindi</option>
                    <option value="hu">Hungarian</option>
                    <option value="id">Indonesian</option>
                    <option value="ga">Irish</option>
                    <option value="it">Italian</option>
                    <option value="ja">Japanese</option>
                    <option value="kn">Kannada</option>
                    <option value="kk">Kazakh</option>
                    <option value="rw_RW">Kinyarwanda</option>
                    <option value="ko">Korean</option>
                    <option value="ky_KG">Kyrgyz (Kyrgyzstan)</option>
                    <option value="lo">Lao</option>
                    <option value="lv">Latvian</option>
                    <option value="lt">Lithuanian</option>
                    <option value="mk">Macedonian</option>
                    <option value="ms">Malay</option>
                    <option value="ml">Malayalam</option>
                    <option value="mr">Marathi</option>
                    <option value="nb">Norwegian</option>
                    <option value="fa">Persian</option>
                    <option value="pl">Polish</option>
                    <option value="pt_BR">Portuguese (Brazil)</option>
                    <option value="pt_PT">Portuguese (Portugal)</option>
                    <option value="pa">Punjabi</option>
                    <option value="ro">Romanian</option>
                    <option value="ru">Russian</option>
                    <option value="sr">Serbian</option>
                    <option value="sk">Slovak</option>
                    <option value="sl">Slovenian</option>
                    <option value="es">Spanish</option>
                    <option value="es_AR">Spanish (Argentina)</option>
                    <option value="es_ES">Spanish (Spain)</option>
                    <option value="es_MX">Spanish (Mexico)</option>
                    <option value="sw">Swahili</option>
                    <option value="sv">Swedish</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                    <option value="th">Thai</option>
                    <option value="tr">Turkish</option>
                    <option value="uk">Ukrainian</option>
                    <option value="ur">Urdu</option>
                    <option value="uz">Uzbek</option>
                    <option value="vi">Vietnamese</option>
                    <option value="zu">Zulu</option>
                    <!-- Add other languages here -->
                  </select>
                </div>

              </div>

              


              <h4 class="text-green-800"><b>Content</b></h4>
              <p class="text-sm mb-2 ">Fill in the header, body and footer sections of your template.</p>

              <div class="bg-[#f5f6fa] p-4">

                <div>
                  <label class="block text-sm font-medium">Header</label>
                  <select v-model="headerMediaComponent.format" class="border border-[#ddd] p-2 rounded-md w-full mb-2">
                    <option value="TEXT">Text</option>
                    <option value="IMAGE">Image</option>
                    <option value="VIDEO">Video</option>

                  </select>

                  <div v-if="headerMediaComponent.format === 'TEXT'">
                    <input v-model="headerComponent.text" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
                  </div>

                  <div v-if="headerMediaComponent.format === 'IMAGE' || headerMediaComponent.format === 'VIDEO'">
                    <div class="flex ml-4 place-items-stretch justify-between w-full">
                      <input type="file" @change="handleFileChange" class="mb-4">

                      <div>
                        <button @click="uploadFile" :disabled="!selectedFile || isUploading"
                          class="mr-5 px-4 py-2 bg-green-700 hover:bg-green-800 text-white rounded-lg disabled:cursor-not-allowed">
                          {{ isUploading ? 'Uploading...' : 'Upload' }}{{ uploadResponse ? 'ed' : '' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium">Body<span class="text-red-800">*</span></label>

                  <textarea v-model="bodyComponent.text" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-30"
                    placeholder="Enter text" rows="4" required></textarea>

                  <div v-if="warningData"
                    class="mt-2 p-3 bg-yellow-100 text-yellow-800 text-sm rounded-md border border-yellow-300">
                    <p class="font-semibold">Warning:{{ warningData }}</p>
                  </div>
                </div>

                <!-- <div class="quill-editor-wrapper">
                                  <QuillEditor class="quill-custom mt-1 p-2 w-full rounded-md h-60 bg-white"
                                   ref="myQuillEditor"
                  v-model:content="bodyComponent.text" contentType="html" theme="snow" :toolbar="[
                    ['bold', 'italic', 'underline']
                  ]" placeholder="Start typing your content here..." />

                </div> -->



                <div class="flex items=flex-end justify-end">
                  <button type="button" @click="addVariable" class="text-black p-2 text-xs font-bold hover:bg-gray-200">
                    + Add variable
                  </button>
                </div>



                <!-- <div v-if="variableCounter">
                <h4>Variable Examples</h4>
                <div v-for="index in variableCounter" :key="index">
                  <input type="text" :placeholder="'Variable ' + index" v-model="variables[index - 1]"
                    class="border border-[#ddd] p-2 rounded-md w-50px mb-2" />
                </div>
              </div> -->

                <div v-if="variables.length">

                  <h4></h4>
                  <label class="block text-sm font-medium">Samples for body content<span class="text-red-800">*</span></label>
                  <span class="text-sm text-gray-500">To help us review your message template, please add an example for each variable in your body text. Do not use real customer information. Cloud API hosted by Meta reviews templates and variable parameters to protect the security and integrity of our services.</span>
                  
                  <div v-for="(variable, index) in variables" :key="index">
                    <input type="text" :placeholder="'Variable ' + (index + 1)" v-model="variables[index]"
                      class="border border-[#ddd] p-2 rounded-md w-50px mb-2" required />
                  </div>
                </div>


                <label class="block text-sm font-medium">Footer</label>
                <input v-model="footerComponent.text" placeholder="Enter text"
                  class="border border-[#ddd] p-2 rounded-md w-full mb-2" />


              </div>

              <h4 class="text-green-800 mt-2"><b>Buttons</b></h4>
              <p class="text-sm mb-2 ">Create buttons that let customers respond to your message or take action.</p>
              <div class="bg-[#f5f6fa] p-4 ">
                  <span>
                  <button class="text-black p-2 text-small border border-black hover:bg-gray-200"
                    @click.prevent="addbutton">
                     + Add Button
                  </button>
                </span>
                <!-- Button Text and URL Inputs -->
                 <div class="mt-2">
                                  <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text"
                  placeholder="Text" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
                <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url"
                  placeholder="URL" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
                 </div>

              </div>


              <!-- Actions -->

              <button @click.prevent="submitTemplate"
                class="bg-green-700 mt-4 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center "
                :disabled="loading || isSubmitted">
                <span v-if="loading"
                  class="animate-spin border-2 border-white border-t-transparent rounded-full w-4 h-4 mr-2"></span>
                {{ isSubmitted ? "Submitted" : loading ? "Submitting..." : "Submit" }}
              </button>

            </form>
          </div>

          <div
            class="flex flex-col flex-grow h-full overflow-y-auto aspect-[10/19] min-w-[320px] p-3 max-h-[600px]  bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center custom-scrollbar">
            <div class="message">
              <span style="white-space: pre-line;" v-html="preview_data"></span>
            </div>
          </div>
        </div>
      </div>

    </PopUp>


  </div>


</template>

<script>

// import { QuillEditor } from '@vueup/vue-quill';
// import '@vueup/vue-quill/dist/vue-quill.snow.css';
import axios from 'axios';
import PopUp from "../popups/popup";
import { useToast } from 'vue-toastification';
import PopUp_preview from "../popups/template_preview";
import confirmationPopup from '../popups/confirmation';

export default {
  components: {
    // QuillEditor,
    
    PopUp_preview,
    confirmationPopup,
    PopUp
  },
  name: 'BroadCast1',
  props: {
    contactReport: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {

      cursor: false,
      apiUrl: process.env.VUE_APP_API_URL,
      selectedFile: null,
      isUploading: false,
      uploadResponse: null,
      uploadError: null,
      uploadHandleID: null,
      deleteTemplateName: '', // To store the name of the template to be deleted
      showConfirmPopup: false, // State to control the confirmation popup visibility

      // loading
      loading: false, // Add loading state
      isSubmitted: false,
      tableLoading: false,

      showPreview: false,
      preview_data: '',
      tooltipVisible: false,
      tooltipStyles: {
        top: "0px",
        left: "0px",
        width: "170px", // Set square dimensions
        height: "100px",
      },
      templateName: '',
      isTemplateNameValid: true,
      templates: [],
      showPopup: false,
      addButton: false,
      showSelectionPopup: false,
      selectedCategory: 'Marketing',
      selectedSubCategory: '',
      selectedLanguage: 'en_US',
      selectedHeaderFormat: 'TEXT',
      template: {
        name: '',
        components: []
      },
      bodyComponent: {
        type: 'BODY',
        text: ''
      },
      headerComponent: {
        type: 'HEADER',
        format: 'TEXT',
        text: ''
      },
      headerMediaComponent: {
        type: 'HEADER',
        format: '',
        example: {
          header_handle: [
            ''
          ]
        }
      },
      footerComponent: {
        type: 'FOOTER',
        text: ''
      },
      button: {
        type: 'URL',
        text: '',
        url: ''
      },
      nameError: '',

      variableCounter: null,
      variables: [],
      warningData: null, // To store error data from the API
    };
  },



  async mounted() {
    await this.fetchtemplateList();

    // this.preview_data = this.generateTemplatePreview(this.template.components);

    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },

  methods: {

      async showConfirmationPopup(templateName) {
    this.showConfirmPopup = true;
    this.deleteTemplateName = templateName; // Store the template name to be deleted
     // Store the template name to be deleted
  },

    addVariable() {
      // const countWords = (text) => {
      //   if (!text) return 0;
      //   return text.split(/\s+/).filter(word => word.trim().length > 0).length;
      // };

      const text = this.bodyComponent.text || '';
      // const wordCount = countWords(text);

      const currentVariables = text.match(/{{\d+}}/g) || [];
      // const requiredWords = 3 * (currentVariables.length + 1);

      // if (wordCount < requiredWords) {
      //   alert(`The text must have at least ${requiredWords} words to add ${currentVariables.length + 1} variables.`);
      //   return;
      // }

      const nextVariableNumber = currentVariables.length + 1;
      this.bodyComponent.text += ` {{${nextVariableNumber}}}`;

      // 🔧 Update both
      this.variableCounter = nextVariableNumber;

      // 🔧 Extend `variables` array safely
      while (this.variables.length < nextVariableNumber) {
        this.variables.push("");
      }

      console.log("Updated variable counter:", this.variableCounter);
      console.log("Updated variables:", this.variables);
    },


    //  addVariable() {
    //   const nextVariableNumber = (this.bodyComponent.text.match(/{{\d+}}/g) || []).length + 1;
    //   const variableToInsert = ` {{${nextVariableNumber}}}`;

    //   // 1. Get the Quill editor instance using the ref
    //   const quill = this.$refs.myQuillEditor.quill;

    //   if (quill) {
    //     // 2. Get the current cursor selection
    //     const selection = quill.getSelection();

    //     if (selection) {
    //       // If there's a selection, insert the text at the current cursor position
    //       quill.insertText(selection.index, variableToInsert, 'user');
    //       // Move the cursor after the inserted text
    //       quill.setSelection(selection.index + variableToInsert.length, 0);
    //     } else {
    //       // If no selection (e.g., editor not focused), append to the end
    //       quill.insertText(quill.getLength(), variableToInsert, 'user');
    //       // Move the cursor to the very end
    //       quill.setSelection(quill.getLength(), 0);
    //     }

    //     // 3. Update your internal data properties
    //     this.variableCounter = nextVariableNumber;

    //     // Extend `variables` array safely
    //     while (this.variables.length < nextVariableNumber) {
    //       this.variables.push("");
    //     }

    //     console.log("Updated variable counter:", this.variableCounter);
    //     console.log("Updated variables:", this.variables);

    //     // Optional: If this.bodyComponent.text is bound with 'contentType="text"',
    //     // update it from Quill's content after insertion to keep them in sync.
    //     // If using 'html' or 'delta', v-model should handle most sync automatically,
    //     // but for immediate plain text reflection, you might still need this.
    //     // This will only update the text representation, not the rich text.
    //     this.bodyComponent.text = quill.getText();

    //   } else {
    //     console.error("Quill editor instance not found. Make sure the ref is set correctly and the editor is mounted.");
    //     // Fallback or error handling if Quill instance isn't available
    //     // (though this is less likely if ref is correctly used)
    //     this.bodyComponent.text += variableToInsert;
    //   }
    // },




    showpreview(preview) {
      this.showPreview = true;
      this.preview_data = preview;

    },
    addbutton() {
      this.addButton = !this.addButton;
    },

    openPopup() {
      this.showPopup = true;
      this.selectedType = 'MARKETING';  // Ensure Marketing is default when opening
    },


    async fetchtemplateList() {
      const token = localStorage.getItem('token');
      this.cursor = true;
      try {
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
        this.cursor = false;

        // Generate previews for templates
        this.templates = this.templates.map(template => {
          return {
            ...template,
            preview: this.generateTemplatePreview(template.components),
          };
        });
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
      }
    },


    generateTemplatePreview(components) {

      if (!Array.isArray(components)) {
        console.warn("generateTemplatePreview: components is not an array", components);
        return ''; // Return an empty string instead of breaking the app
      }
      let previewMessage = '';

      components.sort((a, b) => {
        const order = { HEADER: 1, BODY: 2, FOOTER: 3, BUTTONS: 4 };
        return (order[a.type] || 5) - (order[b.type] || 5);
      });


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





    replacePlaceholders(bodyText, example) {
      if (!bodyText || !Array.isArray(example) || example.length === 0) return bodyText;

      example.forEach((param, index) => {
        if (param && param.toString().trim() !== '') {
          const placeholder = `${index + 1}`;
          const regex = new RegExp(placeholder, 'g');
          bodyText = bodyText.replace(regex, param.toString().trim());
        }
      });

      return bodyText;
    },






    updateTemplateComponents() {


      const clonedBodyComponent = { ...this.bodyComponent };

      if (this.variables.length > 0) {
        clonedBodyComponent.example = { body_text: this.variables };
      }

      let components = [clonedBodyComponent];

      if (this.headerComponent.text) {
        components.push(this.headerComponent);
      }

      if (
        this.headerMediaComponent.example.header_handle &&
        this.headerMediaComponent.example.header_handle.length > 0 &&
        this.headerMediaComponent.example.header_handle[0] !== ''
      ) {
        components.push(this.headerMediaComponent);
      }

      if (this.footerComponent.text) {
        components.push(this.footerComponent);
      }

      if (this.button.text && this.button.url) {
        components.push({
          type: 'BUTTONS',
          buttons: [this.button]
        });
      }

      this.template.components = components;
      console.log(this.template); // Update template components dynamically
    },

    async submitTemplate() {
      const toast = useToast();
      if (this.nameError) {
        return; // Prevent form submission if there are validation errors
      }

      this.loading = true; // Show loading indicator

      const payload = {
        name: this.template.name,
        components: this.template.components,
        language: this.selectedLanguage,
        category: this.selectedCategory,
        sub_category: this.selectedSubCategory
      };

      const token = localStorage.getItem('token');

      if (!token) {
        console.error('No access token found in local storage');
        return;
      }

      try {
        const response = await axios.post(`${this.apiUrl}/create-template`, payload, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.status >= 200 && response.status < 300) {
          console.log('Template created successfully:', response.data);
          toast.success('Template created successfully');
          this.isSubmitted = true;
          await this.fetchtemplateList();

        } else {
          const errorMessage = response.data.detail || "Unknown error occurred";
          
          // alert(`Error creating template: ${errorMessage}`);
          toast.error(`Error creating template: ${errorMessage}`);
          console.error('Error creating template:', response.data.detail);
        }
      } catch (error) {
        // Handle network errors
        const errorMessage = error.response?.data?.detail?.error?.error_user_msg || error.response?.data?.detail?.error?.message || error.message;
        toast.error(`Request failed: ${errorMessage}`);
        // alert(`Request failed: ${errorMessage}`);
        console.error('Request failed:', error);
      }
      finally {

        this.loading = false; // Hide loading indicator
      }
    },


    // 
validateTemplateName() {
  // Convert to lowercase, replace spaces with underscores, and trim whitespace
  this.template.name = this.template.name
    .toLowerCase()
    .replace(/\s+/g, '_')       // replace spaces with underscores
    .trim();                    // remove leading/trailing whitespace

  const regex = /^[a-z_0-9]+$/;

  if (this.template.name === '') {
    this.nameError = 'Template name is required';
  } else if (!regex.test(this.template.name)) {
    this.nameError = 'Template name must contain only lowercase letters, numbers, and underscores.';
  } else {
    this.nameError = '';
  }
},

    async deleteTemplate(template_name) {
      this.showConfirmPopup = false; // Close the confirmation popup if it's open

      const toast = useToast();
      const token = localStorage.getItem('token');

      try {
        this.tableLoading = true;
        const response = await fetch(`${this.apiUrl}/delete-template/${template_name}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });


        if (response.ok) {
          toast.success("Template deleted successfully");
          await this.fetchtemplateList();
        }
        else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }


      } catch (error) {
        console.error('Error deleting template:', error.response ? error.response.data : error.message);
      }
      finally {
        this.tableLoading = false;
        this.deleteTemplateName = ''; // Clear the template name after deletion
      }

    },

    closePopup() {
      this.showPopup = false;
      this.clearForm();
    },


    clearForm() {
      this.Loading = false;
      this.template.name = '';
      this.isSubmitted = false;
      this.variableCounter = null;
      this.template.components = [];
      this.bodyComponent.text = '';
      this.headerComponent.text = '';
      this.footerComponent.text = '';
      this.button.text = '';
      this.button.url = '';
      this.variables = [];
      this.addButton = false;
      this.selectedCategory = 'Marketing';
      this.selectedSubCategory = '';
      this.selectedLanguage = 'en_US';
      this.nameError = '';
      this.loading = false;
      this.preview_data = '';

    },

    closePreview() {
      this.showPreview = false;
      this.preview_data = '';
    },

    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.uploadError = "No file selected for upload.";
        
        return;
      }

      this.isUploading = true;
      this.uploadResponse = null;
      this.uploadError = null;

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const token = localStorage.getItem("token"); // Adjust based on your auth storage
        const response = await axios.post(`${this.apiUrl}/resumable-upload/`, formData, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        });

        this.uploadResponse = response.data;
        this.headerMediaComponent.example.header_handle[0] = response.data.upload_response?.h || "N/A";
        console.log(this.uploadHandleID);
      } catch (error) {
        this.uploadError = error.response ? error.response.data.detail : "Upload failed";
      } finally {
        this.isUploading = false;
      }
    },

    updateVariablesFromText(newText) {
      const placeholders = newText.match(/{{\d+}}/g) || [];
      const uniquePlaceholders = [...new Set(placeholders.map(p => parseInt(p.match(/\d+/)[0])))];
      const requiredLength = uniquePlaceholders.length;

      if (this.variables.length < requiredLength) {
        while (this.variables.length < requiredLength) {
          this.variables.push('');
        }
      } else if (this.variables.length > requiredLength) {
        this.variables.splice(requiredLength);
      }

      console.log("Updated variables:", this.variables);
    },

    validateTemplateText(newText) {
      const countWords = (text) => {
        if (!text) return 0;
        return text.split(/\s+/).filter(word => word.trim().length > 0).length;
      };

      const text = newText || '';
      const wordCount = countWords(text);
      const currentVariables = text.match(/{{\d+}}/g) || [];
      const variableCount = currentVariables.length;

      if (variableCount > 0) {
        const ratio = (wordCount - 1) / variableCount;
        if (ratio < 3) {
          this.warningData = "This template contains too many variable parameters relative to the message length. You need to decrease the number of variable parameters or increase the message length.";
        } else {
          this.warningData = null;
        }
      } else {
        this.warningData = null;
      }
    }


  },


  watch: {
    templateName() {
      this.validateTemplateName();
    },





    'bodyComponent.text'(newText) {
      this.updateVariablesFromText(newText);
      this.validateTemplateText(newText);
    },


    selectType(type) {
      this.selectedType = type;
      this.showSelectionPopup = false;
      this.showPopup = true;
    },


    closeSelectionPopup() {
      this.showSelectionPopup = false;
    },

    // Watch any changes in template.components and update preview_data
    'template.components': {
      deep: true,
      handler(newComponents) {
        console.log("Updated Components:", newComponents);
        this.preview_data = this.generateTemplatePreview(newComponents);
      }
    },
    // Watch for changes in form inputs and update template.components dynamically
    variables: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    bodyComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    headerComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    headerMediaComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    footerComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    button: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    }
  },

};
</script>

<style scoped>
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

.quill-editor-wrapper .ql-container {
  display: flex;
  flex-direction: column-reverse;
  /* This is the key property! */
  /* You might need to adjust height or other styles based on your layout */
  min-height: 200px;
  /* Example: ensure the editor has some height */
  border: 1px solid #ccc;
  /* Restore border if it gets lost with flexbox */
}

/* Optional: Adjust spacing or appearance */
.quill-editor-wrapper .ql-toolbar {
  border-top: 1px solid #ccc;
  /* Add a top border to the toolbar */
  border-bottom: none;
  /* Remove default bottom border if it exists */
}

.quill-editor-wrapper .ql-editor {
  /* Ensure the editor area expands to fill available space */
  flex-grow: 1;
}


</style>

<!-- <style scoped>

.error {
  border-color: red;
}

.error-message {
  color: red;
  font-size: 0.875em;
  margin-top: 0.5em;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

.CreateTemplateContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.CreateTemplateContainer button {
  margin-left: 805px;
}

.templateList_container {
  background-color: #f5f6fa;
  border-radius: 12px 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.templateList-table {
  width: 100%;
  border-radius: 12px 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
}

th {
  padding: 20px 43px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table td {
  border: 1px solid #ddd;
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.templateList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table tbody {
  background-color: white;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.template-type-options {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.template-type-options button {
  flex: 1;
  padding: 10px;
  border: none;
  background-color: #075e54;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.template-type-options button:hover {
  background-color: #075e54;
}

.discard-button {
  margin-top: 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button {
  background-color: 5;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #218838;
}
</style>  -->

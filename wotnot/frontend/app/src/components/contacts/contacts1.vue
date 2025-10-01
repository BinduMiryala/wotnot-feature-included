<template>
  <div class="content-section m-8 md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold ">Manage Contacts</h2>
        <p class="text-xsm md:text-base">Contact list stores the list of numbers that you've interacted with.
          You can even manually export or import contacts.</p>
      </div>

      <div class="flex justify-between">
        <div>
          <!-- <button @click="showPopup = true"
            class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg">
            + Add Contact
          </button> -->

          <button
            class="bg-green-700 hover:bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center "
            @click="showPopup = true">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
            </svg>
            New Contact
          </button>
        </div>



      </div>


      <confirmationPopup v-if="showConfirmPopup" @yes="deleteContact(this.selectedContact)"
                  @no="showConfirmPopup = false" @close="showConfirmPopup = false" />
      <PopUp1 v-if="showPopupimport" @close="closePopupimport()">

        <h2 class="text-xl font-semibold mb-4">Bulk Import Contacts</h2>
        <hr class="mb-4 border-gray-300">

        <div class="overflow-y-auto max-h-[70vh] p-6 custom-scrollbar space-y-6">

          <!-- File Upload Section -->
          <div class="flex justify-between items-center space-x-4">
            <input type="file" @change="onFileChange" accept=".csv" />
            <button :disabled="!file" @click="uploadFile"
              class="h-8 w-24 border-2 border-green-500 text-green-500 hover:text-white hover:bg-green-500 transition duration-200">
              Upload
            </button>
          </div>

          <!-- Duplicate Contacts Section -->
          <div v-if="duplicates.length">
            <h4 class="text-green-700 font-semibold mb-2">Duplicate Contacts</h4>
            <div class="overflow-y-auto max-h-[30vh] custom-scrollbar">
              <table class="w-full table-fixed border border-gray-300 rounded-lg text-sm md:text-base bg-white">
                <thead>
                  <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[20%]">Name</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[30%]">Email</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[20%]">Phone</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[30%]">Tags</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(contact, index) in duplicates" :key="index">
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.name }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.email }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.phone }}</td>
                    <td class="p-2 text-left border border-gray-200">
                      <div class="truncate" v-for="(value, key) in contact.tags" :key="key">
                        {{ key }}: {{ value }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- New Contacts Section -->
          <div v-if="importcontacts.length">
            <h4 class="text-green-700 font-semibold mb-2">New Contacts</h4>
            <div class="overflow-y-auto max-h-[30vh] custom-scrollbar">
              <table class="w-full table-fixed border border-gray-300 rounded-lg text-sm md:text-base bg-white">
                <thead>
                  <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[20%]">Name</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[30%]">Email</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[20%]">Phone</th>
                    <th class="p-2 border border-gray-300 sticky top-0 z-10 bg-gray-100 w-[30%]">Tags</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(contact, index) in importcontacts" :key="index">
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.name }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.email }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.phone }}</td>
                    <td class="p-2 text-left border border-gray-200">
                      <div class="truncate" v-for="(value, key) in contact.tags" :key="key">
                        {{ key }}: {{ value }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Import Button -->
          <div v-if="importcontacts.length" class="flex justify-end">
            <button :disabled="!file" @click="ImportCSV"
              class="h-8 w-24 border-2 border-green-500 text-green-500 hover:text-white hover:bg-green-500 transition duration-200">
              Import
            </button>
          </div>
        </div>


      </PopUp1>

    </div>
    <PopUpSmall v-if="showPopup" @close="closePopup">
      <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Edit Contact' : 'Add Contact' }}</h2>
      <hr class="mb-4 border-gray-300">
      <form @submit.prevent="submitForm" id="contactForm" class="w-[400px] bg-white">
        <div class="p-4 bg-[#f5f6fa]">
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium">Name<span class="text-red-800">*</span></label>
            <input type="text" v-model="contact.name" id="name" placeholder="Name" required
              class="border border-gray-300 rounded px-3 py-2 w-full">
          </div>

          <div class="mb-4">
            <label for="phone" class="block text-sm font-medium">Phone Number<span class="text-red-800">*</span></label>
            <div class="flex">
              <select v-model="contact.countryCode" class="border border-gray-300 rounded-l px-3 py-2 w-20 mr-2">
                <option value="1">+1</option>
                <option value="44">+44</option>
                <option value="91">+91</option>
              </select>
              <input type="text" v-model="contact.phone" id="phone" placeholder="Phone Number" required
                class="border border-gray-300 rounded-r px-3 py-2 w-full">
            </div>
          </div>
          <label for="email" class="block text-sm font-medium">Email</label>
          <input type="email" v-model="contact.email" id="email" placeholder="Email"
            class="border border-gray-300 rounded px-3 py-2 mb-2 w-full">

          <div class="mb-4">

            <div class="custom-scrollbar tags-container-container">

              <div class="tags-container">
                <div class="tag-input" v-for="(tag, index) in contact.tags" :key="index"
                  style="display: flex; align-items: center;">
                  <input type="text" v-model="tag.key" placeholder="Key" required
                    class="border border-gray-300 rounded px-3 py-2 mb-2 w-full" style="width: 60%;">
                  <input type="text" v-model="tag.value" placeholder="Value" required
                    class="border border-gray-300 rounded px-3 py-2 mb-2 w-full" style="width: 60%; margin-left: 10px;">
                  <button type="button" @click="removeTag(index)" class="hover:bg-gray-100 rounded-full p-2 transition">
                    <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                      colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px"></lord-icon>
                  </button>
                  <span v-if="warningData" class="text-red-500 text-xs">{{ warningData }}</span>
                </div>
              </div>
            </div>
            <button type="button" @click="addTag"
              class="text-black p-2 text-small border border-black hover:bg-gray-200">+ Add
              Tag</button>

          </div>
        </div>


        <div class="flex justify-end pt-4 ">
          <button type="submit" class="bg-green-700 hover:bg-green-600 text-white px-4 py-2 rounded">
            {{ isEditing ? 'Update Contact' : 'Add Contact' }}
          </button>
        </div>
      </form>
    </PopUpSmall>



    <div class=" p-5  filter-container space-x-2">

      <h3 class="text-xl md:text-2xs mb-0 text-gray-600"><b>Contact List</b></h3>




      <div class="flex items-center space-x-2  justify-between">

        <div class="flex items-center space-x-2  justify-between">
          <h3 class="text-l"><b>Filter by tags:</b></h3>

          <input type="text" v-model="tag_key" placeholder="Key"
            class="border border-gray-300 rounded px-3 py-2 w-40px">
          <input type="text" v-model="tag_value" placeholder="Value"
            class="border border-gray-300 rounded px-3 py-2 w-40px">

          <button @click="fiterBytTags"
            class="relative my-2 h-auto w-auto p-2 bg-green-700 hover:bg-green-600 text-white">Apply
            filter</button>
        </div>

        <div>
          <button @click="showPopupimport = true" class="bg-green-600 hover:bg-green-600 text-white px-4 py-2 ">
            <i class="bi bi-download"></i> Import CSV
          </button>
        </div>
      </div>
    </div>



    <div class="overflow-x-auto max-h-[51vh] custom-scrollbar">
      <table class="w-full border border-gray-300 rounded-lg text-sm md:text-base bg-white">
        <thead>
          <tr class="bg-gray-100 text-center text-gray-700 font-semibold">
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">ID</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Name</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Phone Number</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Email</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Tags</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Created At</th>
            <th class="p-3 md:p-4 border border-gray-300 sticky top-0 z-10 bg-gray-100">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in contacts" :key="contact.id" class="hover:bg-gray-50">
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ contact.id }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ contact.name }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ contact.phone }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ contact.email }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <div v-for="(tag, index) in contact.tags" :key="index">
                <span class="font-semibold">{{ tag.key }}:</span> {{ tag.value }}
              </div>
            </td>
            <td class="p-3 md:p-4 text-center border border-gray-200">{{ formatDate(contact.created_at) }}</td>
            <td class="p-3 md:p-4 text-center border border-gray-200">
              <div class="flex justify-center space-x-2">
                <button @click="modifyContact(contact)" class="hover:bg-white rounded-full p-2 transition">
                  <lord-icon src="https://cdn.lordicon.com/wuvorxbv.json" trigger="hover"
                    style="width:32px;height:32px">
                  </lord-icon>
                </button>
                

                <button @click="showConfirmationPopup(contact.phone)" class="hover:bg-white rounded-full p-2 transition">
                  <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                    colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                  </lord-icon>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>



    <div class="flex justify-center mt-4">
      <div class="flex items-center space-x-4 bg-white shadow-md rounded-lg px-4 py-2">
        <button
          class="px-3 py-1 bg-green-600 text-white font-medium rounded hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="loadPreviousPage" :disabled="currentPage === 1">
          Previous
        </button>
        <div class="px-4 py-1 border border-gray-300 rounded text-gray-700 font-semibold">
          {{ currentPage }}
        </div>
        <button class="px-3 py-1 bg-green-600 text-white font-medium rounded hover:bg-green-600" @click="loadNextPage">
          Next
        </button>
      </div>
    </div>

  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp1 from "../popups/popup1";
import PopUpSmall from "../popups/popup_small";
import confirmationPopup from '../popups/confirmation';

import axios from "axios";

export default {
  components: {
    PopUp1,
    PopUpSmall,
    confirmationPopup
  },
  async mounted() {
    await this.fetchContactList();


    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  name: "ContActs1",
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      currentPage: 1,
      showPopup: false,
      showPopupimport: false,
      showActionPopup: false,
      showConfirmPopup: false,
      file: null,
      importcontacts: [], // Initialize as an empty array
      duplicates: [], // Initialize as an empty array
      contact: {
        id: "",
        name: "",
        email: "",
        phone: "",
        countryCode: "",
        tags: [],

        // Search Bar
        tag_key: '',
        tag_value: '',
      },
      selectedContact: null,
      contacts: [],
      isEditing: false,
      searchQuery: '',  // This will be used for searching by phone number
      selectedTag: null,
      sortBy: 'updated_at', // Default sorting criteria
      order: 'desc', // Default sorting order
      searchTerm: '',
      warningData: '',// For searching by contact name
    };
  },
  computed: {
    filteredContacts() {
      const searchPhone = this.searchQuery.toLowerCase(); // Updated to use searchQuery for phone numbers
      const searchName = this.searchTerm.toLowerCase(); // For contact name search

      return this.contacts
        .filter(contact => {
          const matchesPhone = contact.phone.toLowerCase().includes(searchPhone); // Searching by phone number
          const matchesName = contact.name.toLowerCase().includes(searchName); // Searching by contact name
          const matchesTag = this.selectedTag
            ? contact.tags.some(tag => tag.key.toLowerCase() === this.selectedTag.toLowerCase())
            : true;
          return (matchesPhone || matchesName) && matchesTag; // Filtering by phone number, name, and tags
        });
    },
    uniqueTags() {
      const allTags = this.contacts.flatMap(contact => contact.tags.map(tag => tag.key));
      return [...new Set(allTags)];
    },
    formattedTags() {
      return this.contacts.map(contact => ({
        ...contact,
        formattedTags: contact.tags.map(tag => `${tag.key}: ${tag.value}`).join(', '),
      }));
    }
  },
  methods: {

    showConfirmationPopup(phone) {
      this.selectedContact = phone;
      this.showConfirmPopup = true; // Show the confirmation popup
    },

    async loadNextPage() {
      const prev = this.contacts[0]?.id
      await this.fetchContactList(this.currentPage + 1);
      const newFirst = this.contacts[0]?.id;
      if (prev !== newFirst && this.contacts.length > 0) {
        this.currentPage += 1;
      }

    },
    async loadPreviousPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        await this.fetchContactList(this.currentPage);
      }
    },

    async submitForm() {
      const toast = useToast();
      const { id, name, email, phone, countryCode, tags } = this.contact;

      let fullPhoneNumber = phone;
      if (countryCode && countryCode.trim() !== '') {
        fullPhoneNumber = `${countryCode}${phone}`;
      }

      if (tags.some(tag => tag.key === '' || tag.value === '')) {
        this.warningData = "Please enter key and value for all tags";
        return;
      }

      const tagArray = tags.map(tag => `${tag.key}:${tag.value}`);

      const url = id ? `${this.apiUrl}/contacts/${id}` : `${this.apiUrl}/contacts/`;
      const method = id ? "PUT" : "POST";
      const token = localStorage.getItem("token");

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name, email, phone: fullPhoneNumber, tags: tagArray }), // Send full phone number
        });

        if (response.ok) {
          toast.success(id ? "Contact updated successfully" : "Contact created successfully");
          this.clearForm();
          this.fetchContactList();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error saving contact:", error);
        toast.error("Error saving contact");
        
      }
    },
    clearForm() {
      this.contact = {
        id: "",
        name: "",
        email: "",
        phone: "",
        tags: [],
      };
      this.showPopup = false;
    },
    closePopup() {
      this.showPopup = false;
      this.clearForm();  // Clear the form when closing the 
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', options).replace(/,/g, '');
    },


async fetchContactList(page = 1) {
  const token = localStorage.getItem("token");
  const itemsPerPage = 10; // Number of contacts per page
  // Modified URL to explicitly sort by 'created_at' in 'desc' (descending) order
  const url = `${this.apiUrl}/contacts/?sort_by=updated_at&order=desc&limit=${itemsPerPage}&offset=${(page - 1) * itemsPerPage}`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const contactsList = await response.json();
    console.log(contactsList);

    if (contactsList.length === 0) {
      return;
    }
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
  } catch (error) {
    console.error("Error fetching contacts:", error);
  }
},

    // Contacts Tags Filter
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
    closeActionPopup() {
      this.showActionPopup = false;
      this.selectedContact = null;
    },
    modifyContact(contact) {
      this.isEditing = true; // Set to true for editing mode
      this.selectedContact = contact;
      this.contact = { ...this.selectedContact };
      this.showPopup = true;
      this.closeActionPopup();
    },
    async deleteContact(phone) {
      const toast = useToast();
      this.showConfirmPopup = false; // Close the confirmation popup


      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`${this.apiUrl}/contacts/${phone}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          toast.success("Contact deleted successfully");
          this.fetchContactList();
          this.closeActionPopup();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error deleting contact:", error);
        toast.error("Error deleting contact");
        
      }
    },




    addTag() {
      this.warningData = ""; // Reset warning message
      const lastTag = this.contact.tags[this.contact.tags.length - 1];
      if (this.contact.tags.length === 0 || (lastTag.key !== '' && lastTag.value !== '')) {
        this.contact.tags.push({ key: "", value: "" });
      } else {
        this.warningData = "Please enter key and value for the previous tag";
      }
    },
    removeTag(index) {
      this.contact.tags.splice(index, 1);
    },
    filterContacts() {
      this.fetchContactList();
    },

    onFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      if (!this.file) return;

      const formData = new FormData();
      const token = localStorage.getItem("token");
      formData.append("file", this.file);

      try {
        const response = await axios.post(`${this.apiUrl}/contacts/csv/`, formData, {
          headers: { "Content-Type": "multipart/form-data", Authorization: `Bearer ${token}` },
        });

        // Update the table with imported contacts
        this.importcontacts = response.data.contacts || [];
        this.duplicates = response.data.duplicates || [];
      } catch (error) {
        console.error("Error importing contacts:", error.response?.data?.detail || error.message);
      }
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
          this.fetchContactList();
        } else {
          toast.error(`Error: ${response.data?.detail || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error importing contacts:", error.response?.data?.detail || error.message);
        toast.error(`Error: ${error.response?.data?.detail || "Something went wrong"}`);
      }
    },

    closePopupimport() {
      this.showPopupimport = false;
      this.file = null;
      this.importcontacts = [];
      this.duplicates = [];
    },

  },
};
</script>

<style scoped>
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

.tags-container {
  max-height: 120px;
  /* adjust this value based on the height of your attribute rows */
  overflow-y: auto;
}

.tags-container::-webkit-scrollbar {
  width: 8px;
}

.tags-container::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.tags-container::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.tags-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}




.name-column {
  max-width: 130px;
  /* Adjust based on your needs */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-id-column {
  font-size: 1.0rem;
  /* Adjust the font size as needed */
  max-width: 20px;
  /* Optional: Adjust width if needed */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


</style>










<!-- <div class="mb-4">
          <label for="attributes" class="block text-sm font-medium">Custom Attribute (Optional)</label>
          <button @click="addAttribute" type="button" class="border border-green-500 text-green-500 px-4 py-2 rounded">
            + Add Attribute
          </button>
        </div> -->

<!-- <PopUpSmall v-if="showActionPopup" @close="closeActionPopup">
      <div class="bg-white shadow-lg rounded-lg p-4">
        <p class="text-lg mb-4">What action do you want to take?</p>
        <div class="flex space-x-4">
          <button @click="modifyContact" class="bg-yellow-500 text-white py-2 px-4 rounded">Modify</button>
          <button @click="deleteContact(selectedContact.phone)"
            class="bg-red-500 text-white py-2 px-4 rounded">Delete</button>
        </div>
      </div>
    </PopUpSmall> -->
<!-- <button @click="openActionPopup(contact)"
                  class="bg-[#075e54] text-white py-2 px-4 rounded">Action
                </button> -->
















<!-- <style scoped>
 .contactsListContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}

.contactsList-table {
  width: 100%;
  border-radius: 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.contactsList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.contactsList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.contactsList-table tbody {
  background-color: white; 
}


</style>  -->

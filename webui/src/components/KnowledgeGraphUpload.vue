<template>
  <div class="kg-upload-section">
    <h2>Upload Knowledge Graph</h2>
    <div class="upload-container">
      <input 
        type="file" 
        ref="fileInput"
        @change="handleFileSelect"
        accept=".rdf,.owl,.ttl,.n3,.nt,.jsonld,.xml"
        class="file-input"
      />
      <button 
        @click="uploadFile" 
        :disabled="!selectedFile || uploading"
        class="upload-btn"
      >
        {{ uploading ? 'Uploading...' : 'Upload & Replace Knowledge Graph' }}
      </button>
      
      <div v-if="selectedFile" class="file-info">
        <p>Selected: {{ selectedFile.name }}</p>
        <p>Format: {{ detectFormat(selectedFile.name) }}</p>
      </div>
      
      <div v-if="uploadStatus.message" 
           :class="['status-message', uploadStatus.type]">
        {{ uploadStatus.message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../services/axios.js';

export default {
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadStatus: {
        message: '',
        type: '' // 'success' or 'error'
      }
    }
  },
  
  methods: {
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
      this.uploadStatus = { message: '', type: '' };
    },
    
    detectFormat(filename) {
      const ext = filename.split('.').pop().toLowerCase();
      const formats = {
        'rdf': 'RDF/XML',
        'owl': 'OWL/RDF',
        'ttl': 'Turtle',
        'n3': 'Notation3',
        'nt': 'N-Triples',
        'jsonld': 'JSON-LD',
        'xml': 'RDF/XML'
      };
      return formats[ext] || 'Unknown';
    },
    
    async uploadFile() {
      if (!this.selectedFile) return;
      
      this.uploading = true;
      this.uploadStatus = { message: '', type: '' };
      
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      
      try {
        const response = await axios.post(
          '/ontology/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        this.uploadStatus = {
          message: `Success! ${response.data.message}`,
          type: 'success'
        };
        
        // Emit event to parent to refresh data
        this.$emit('ontologyUploaded');
        
        // Clear file input
        this.$refs.fileInput.value = '';
        this.selectedFile = null;
        
      } catch (error) {
        this.uploadStatus = {
          message: `Error: ${error.response?.data?.error?.message || error.message}`,
          type: 'error'
        };
      } finally {
        this.uploading = false;
      }
    }
  }
}
</script>

<style scoped>
.kg-upload-section {
  width: 90%;
  margin: 50px auto;
}

.kg-upload-section h2 {
  font-family: "Poppins";
  font-size: 48px;
  font-weight: 700;
  margin: 30px 0;
  text-align: left;
}

.upload-container {
  display: flex;
  flex-direction: column;
  align-items: left;
  gap: 1.5rem;
  width: 100%;
}

.file-input {
  padding: 0.75rem;
  border: 2px dashed #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-family: "Poppins";
  font-size: 12px;
  width: 100%;
  max-width: 500px;
}

.upload-btn {
  background-color: #FFEE8C;
  font-family: "Poppins";
  font-size: 18px;
  font-weight: 700;
  border: 2px solid #000;
  border-radius: 30px;
  padding: 10px 50px;
  cursor: pointer;
  color: #000;
  width: 100%;
  max-width: 530px;
}

.upload-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.file-info {
  padding: 1rem;
  background: #e3f2fd;
  border-radius: 8px;
  font-family: "Poppins";
  font-size: 18px;
  text-align: left;
  max-width: 500px;
}

.file-info p {
  margin: 0.25rem 0;
  font-family: "Poppins";
}

.status-message {
  padding: 1rem;
  border-radius: 8px;
  font-family: "Poppins";
  font-size: 18px;
  text-align: left;
  max-width: 500px;
}

.status-message.success {
  background: #d4edda;
  color: #155724;
}

.status-message.error {
  background: #f8d7da;
  color: #721c24;
}
</style>
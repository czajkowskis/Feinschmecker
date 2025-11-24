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
      
      // Target format is RDF/XML (best OWLReady2 support)
      formData.append('target_format', 'xml');
      
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
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin: 2rem 0;
}

.upload-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 500px;
}

.file-input {
  padding: 0.5rem;
  border: 2px dashed #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.upload-btn {
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.upload-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.file-info {
  padding: 0.5rem;
  background: #e3f2fd;
  border-radius: 4px;
}

.status-message {
  padding: 0.75rem;
  border-radius: 4px;
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
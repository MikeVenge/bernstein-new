# Field Mapper Full-Stack Application

A modern web application for parameterized Excel field mapping with Python backend and React frontend.

## 🏗️ Architecture

- **Backend**: Python FastAPI with file upload, processing, and download APIs
- **Frontend**: React with Tailwind CSS for modern, responsive UI
- **Deployment**: Ready for Vercel (frontend) and Railway (backend)

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start backend server**:
   ```bash
   python main.py
   ```
   
   Backend will run at: `http://localhost:8000`
   API docs available at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```
   
   Frontend will run at: `http://localhost:3000`

## 📱 Application Features

### 1. **File Upload Interface**
- Drag & drop support for Excel and CSV files
- File validation and size limits
- Progress indicators

### 2. **Mapping Configuration**
- **Target Column**: Choose destination column (71 = BS, 75 = BW, etc.)
- **Data Column**: Choose source column (CO, BR, BS, etc.)
- Visual data flow representation
- Mapping preview with statistics

### 3. **Execution Monitoring**
- Real-time progress tracking
- Status updates and error handling
- Results summary with detailed statistics

### 4. **Results Download**
- Download populated Excel file
- Download audit trail CSV
- Download all files as ZIP archive
- Job cleanup functionality

## 🔧 Parameter Clarification

### `--column` (DESTINATION)
- **Purpose**: Where to write data in destination file
- **Example**: `--column 75` = Column 75 (BW)

### `--data-column` (SOURCE)
- **Purpose**: Where to read data from source file  
- **Example**: `--data-column "BR"` = Column BR (70)

### Data Flow:
```
SOURCE FILE                    DESTINATION FILE
Column BR (--data-column)  →   Column 75 (--column)
```

## 📊 Supported File Types

### Input Files:
- **Source File**: Excel (.xlsx) containing source data
- **Destination File**: Excel (.xlsx) to populate
- **Mapping File**: CSV with field relationships

### Output Files:
- **Populated Excel**: Destination file with mapped data
- **Audit Trail**: CSV log of all operations
- **Source Tracking**: Automatic source location tracking

## 🎯 Generic Mapping Format

The application uses a generic mapping format that focuses on **field relationships** rather than specific data values:

### Key Features:
- **Reusable**: Works across different time periods
- **Portable**: Adaptable for different companies
- **Transformation-Aware**: Handles composite fields, percentage conversions
- **Validation Methods**: Multiple verification strategies

### Sample Generic Mapping:
```csv
Dest_Row,Dest_Field,Source_Sheet,Source_Row,Source_Field,Mapping_Type,Transformation
12,United States and other North America,Key Metrics,6,North America,Geographic_Translation,DIRECT_COPY
140,Accrued expenses and other liabilities,Balance Sheet,30+31+32+33,Composite field,Composite_Match,SUM_FIELDS
```

## 🌐 Deployment

### Vercel (Frontend)
1. Connect GitHub repository to Vercel
2. Set build directory to `frontend`
3. Configure environment variables for API URL

### Railway (Backend)
1. Connect GitHub repository to Railway
2. Set root directory to `backend`
3. Configure Python buildpack
4. Set environment variables

### Environment Variables:
```bash
# Backend
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# Frontend  
REACT_APP_API_URL=https://your-backend.railway.app
```

## 🧪 Testing

### Backend Testing:
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing:
```bash
cd frontend
npm test
```

### API Testing:
Visit `http://localhost:8000/docs` for interactive API documentation

## 📈 Usage Flow

1. **Upload Files**: Source Excel, Destination Excel, Mapping CSV
2. **Configure Parameters**: Set target and data columns
3. **Execute Mapping**: Run field mapping process
4. **Download Results**: Get populated files and audit trail

## 🎯 Benefits

- **User-Friendly**: Modern web interface with step-by-step workflow
- **Flexible**: Parameterized for different use cases
- **Traceable**: Complete audit trail and source tracking
- **Scalable**: Ready for cloud deployment
- **Maintainable**: Clean separation of concerns

The application transforms the command-line field mapping tool into a modern web application suitable for business users while maintaining all the advanced mapping capabilities.

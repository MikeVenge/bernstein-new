#!/bin/bash

echo "🚀 Starting Field Mapper Full-Stack Application"
echo "=============================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected directories: backend/ and frontend/"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ All prerequisites found"

# Setup backend
echo ""
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start backend in background
echo "Starting backend server on port 8000..."
python main.py &
BACKEND_PID=$!

cd ..

# Setup frontend
echo ""
echo "⚛️ Setting up frontend..."
cd frontend

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend
echo "Starting frontend server on port 3000..."
npm start &
FRONTEND_PID=$!

cd ..

# Display startup information
echo ""
echo "🎉 Field Mapper application started successfully!"
echo "=============================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Parameter clarification:"
echo "   --column = DESTINATION column (where to write)"
echo "   --data-column = SOURCE column (where to read)"
echo ""
echo "🛑 To stop the application:"
echo "   Press Ctrl+C or run: ./stop_local_dev.sh"
echo ""

# Create stop script
cat > stop_local_dev.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping Field Mapper application..."

# Kill processes by port
echo "Stopping backend (port 8000)..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

echo "Stopping frontend (port 3000)..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

echo "✅ Application stopped"
EOF

chmod +x stop_local_dev.sh

# Wait for user to stop
echo "Press Ctrl+C to stop both servers..."
wait
